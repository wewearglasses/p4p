import boto3
import os
import json
import uuid
import config
from flask import Flask, render_template, request

rek = boto3.client('rekognition',
                   aws_access_key_id=config.AWS_KEY,
                   aws_secret_access_key=config.AWS_SECRET,
                   region_name='us-west-2')

s3 = boto3.resource('s3', aws_access_key_id=config.AWS_KEY,
                    aws_secret_access_key=config.AWS_SECRET,
                    region_name='us-west-2')

app = Flask('p4p')


@app.route('/')
def take_photo():
    return render_template('take-photo.html')


@app.route('/faces')
def list_faces():

    return render_template('faces.html', faces=json.load(open('faces.json')))


@app.route('/upload-photo', methods=['POST'])
def upload():
    db = json.load(open('db.json'))
    filename = uuid.uuid4().hex+'.jpg'
    if db.get(filename):
        del db[filename]
    file_obj = request.files['image']
    obj = s3.Object(config.BUCKET, filename)
    metadata = {'CacheControl': 'max-age=9999', 'ContentType': 'image/jpeg'}
    obj.upload_fileobj(file_obj, ExtraArgs=metadata)
    obj.Acl().put(ACL='public-read')
    # Read faces.json
    # Build dictionary of {"id":"name"}
    # Call rekognition to detect faces
    # for each face id, get the name of the face
    # db[filename]={"faces":[names]}
    # save the result to data/filename.json
    # save db.json
    db[filename] = {}

    json.dump(db, open('db.json', 'w'), indent=2)
    return 'ok'


@app.route('/update-face', methods=['POST'])
def update_face():
    faces = json.load(open('faces.json'))
    name = request.form['name']
    filename = name+'.jpg'
    file_obj = request.files['image']
    obj = s3.Object(config.BUCKET, filename)
    metadata = {'CacheControl': 'max-age=9999', 'ContentType': 'image/jpeg'}
    obj.upload_fileobj(file_obj, ExtraArgs=metadata)
    obj.Acl().put(ACL='public-read')

    # read faces.json
    # delete old faceid
    # call rekognition to index face
    # save face id
    # update faces.json
    # save it
    return 'ok'


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(port=8080, debug=True)