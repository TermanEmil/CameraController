function camerasAutodetect() {
    $.ajax({
        url: '/api/cameras_autodetect',

        success: function() {
            location.reload();
        },

        error: function(data) {
            alert('Failed to detect cameras. Error: ' + data.responseText);
        }
    });
}