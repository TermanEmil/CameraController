function cameraRemoveBtnClick(cameraId) {
    $.ajax({
        url: '/api/camera_remove/' + cameraId,

        success: function() {
            location.reload();
        },

        error: function(data) {
            alert('Failed to remove camera ' + cameraId + '. Error: ' + data.responseText);
        }
    })
}