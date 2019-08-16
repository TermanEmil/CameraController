function cameraCaptureImgBtnClick(element, cameraId) {
    var iconElement = element.getElementsByTagName("i")[0];
    var iconClassNameSave = iconElement.className;

    elementOnClickSave = element.onclick;
    element.onclick = null;

    iconElement.className = "fa fa-fw fa-spinner fa-spin";

    // Download the file. The filename is expected to be in the content's type (:
    $.ajax({
        url: '/api/camera_capture_img_and_download/' + cameraId,
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
        },

        error: function(data) {
            msg = "Failed to capture picture: " + data.responseText;
            alert(msg);
        },
    }).always(function() {
        iconElement.className = iconClassNameSave;
        element.onclick = elementOnClickSave;
    });
}