function removeCamera(cameraId) {
    $.ajax({
        url: '/camera_control/camera_remove/' + cameraId,
        dataType: 'json',
        success: function(data) {
            location.reload();
        }
    });
}

function cameraReconnect(element, cameraId) {
    var iconElement = element.getElementsByTagName("i")[0];
    var iconClassNameSave = iconElement.className;

    elementOnClickSave = element.onclick;
    element.onclick = null;

    iconElement.className = "fa fa-fw fa-spinner fa-spin";

    $.ajax({
        url: '/camera_control/camera_reconnect/' + cameraId,
    })
    .always(function() {
        iconElement.className = iconClassNameSave;
        element.onclick = elementOnClickSave;
    })
    .fail(function(data) {
        msg = "Failed to reconnect: " + data["statusText"] + ": " + data["status"];
        alert(msg);
    });
}

function captureImg(element, cameraId) {
    var iconElement = element.getElementsByTagName("i")[0];
    var iconClassNameSave = iconElement.className;

    elementOnClickSave = element.onclick;
    element.onclick = null;

    iconElement.className = "fa fa-fw fa-spinner fa-spin";

    // Download the file. The filename is saved in the content's type.
    $.ajax({
        url: '/camera_control/capture_img_and_download/' + cameraId,
        xhrFields: {
            responseType: 'blob'
        },

        success: function(data) {
            var url = window.URL.createObjectURL(data);
            var a = document.createElement('a');

            a.href = url;
            a.download = data['type'];
            a.style.display = "none";
            document.body.append(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        }
    })
    .always(function() {
        iconElement.className = iconClassNameSave;
        element.onclick = elementOnClickSave;
    })
    .fail(function(data) {
        msg = "Failed to capture a picture: " + data["statusText"] + ": " + data["status"];
        alert(msg);
    });
}