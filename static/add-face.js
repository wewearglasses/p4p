function name_changed(ele) {
    var val = ele.value.trim();
    if (val.length > 2) {
        $(".icon-camera").removeClass("d-none");
    } else {
        $(".icon-camera").addClass("d-none");
    }
}

for (var ele of document.querySelectorAll("input[type=file]")) {
    ele.onchange = function(e) {
        var name = $(e.target)
            .closest(".face")
            .attr("name");
        loadImage(
            e.target.files[0],
            img => {
                let canvas = to_canvas(img);
                canvas.toBlob(b => do_upload(b, name), "image/jpeg", 0.85);
            },
            { maxWidth: 2000, maxHeight: 2000, orientation: true, canvas: true }
        );
    };
}

function to_canvas(image) {
    if (image.tagName == "IMG") {
        let imgCanvas = document.createElement("canvas");
        let imgContext = imgCanvas.getContext("2d");

        // Make sure canvas is as big as the picture
        imgCanvas.width = image.width;
        imgCanvas.height = image.height;

        // Draw image into canvas element
        imgContext.drawImage(image, 0, 0, image.width, image.height);
        return imgCanvas;
    } else {
        return image;
    }
}

function do_upload(image_data, name) {
    $(".icon-camera").html("Uploading...");
    $(".icon-camera").css("background", "none");
    $("input").detach();
    let fd = new FormData();
    fd.set("image", image_data, "image.jpg");
    fd.set("name", name);
    $.ajax({
        type: "POST",
        url: "/update-face",
        data: fd,
        processData: false,
        contentType: false,
        xhr: function() {
            var xhr = new window.XMLHttpRequest();
            return xhr;
        },
        complete: evt => {
            $(".icon-camera").html("<h2>Done!</h2><p>Go and take some photos now</p>");
        }
    });
}
