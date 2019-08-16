function favFieldRemoveBtnClick(url, csrf_token) {
    $.ajax({
        url: url,
        type: 'delete',

        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },

        success: function(result) {
            location.reload();
        },

        error: function(data) {
            alert('Failed to remove favourite config. Error: ' + data.responseText);
        }
    });
}