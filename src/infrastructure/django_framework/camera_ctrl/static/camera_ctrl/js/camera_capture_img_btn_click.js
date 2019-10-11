function cameraCaptureImgBtnClick(element, cameraId) {
    urlToSend = '/api/camera_capture_img_and_download/' + cameraId;

    var iconElement = element.getElementsByTagName("i")[0];
    var iconClassNameSave = iconElement.className;

    elementOnClickSave = element.onclick;
    element.onclick = null;

    iconElement.className = "fa fa-fw fa-spinner fa-spin";

    $.ajax({
        url: '/api/camera_capture_img_and_download/' + cameraId,
        xhrFields: {
            responseType: 'blob'
        },

        success: function(response, status, xhr) {
            var filename = "";
            var disposition = xhr.getResponseHeader('Content-Disposition');
            if (disposition && disposition.indexOf('attachment') !== -1) {
                var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                var matches = filenameRegex.exec(disposition);

                if (matches != null && matches[1])
                    filename = matches[1].replace(/['"]/g, '');
            }

            var url = window.URL.createObjectURL(response);
            var a = document.createElement('a');

            a.href = url;
            a.download = filename;
            a.style.display = "none";
            document.body.append(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        },

        error: function(response, status, xhr) {
            alert('Failed to capture picture: ' + xhr);
            console.log(response);
        }
    }).always(function() {
        iconElement.className = iconClassNameSave;
        element.onclick = elementOnClickSave;
    });
}