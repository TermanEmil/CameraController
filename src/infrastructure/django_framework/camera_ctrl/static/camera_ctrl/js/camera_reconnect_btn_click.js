function cameraReconnectBtnClick(element, cameraId) {
    var iconElement = element.getElementsByTagName("i")[0];
    var iconClassNameSave = iconElement.className;

    elementOnClickSave = element.onclick;
    element.onclick = null;

    iconElement.className = "fa fa-fw fa-spinner fa-spin";

    $.ajax({
        url: '/api/camera_reconnect/' + cameraId,

        error: function(data) {
            alert('Failed to reconnect camera ' + cameraId + '. Error: ' + data.responseText);
        }
    }).always(function() {
        iconElement.className = iconClassNameSave;
        element.onclick = elementOnClickSave;
    });
}