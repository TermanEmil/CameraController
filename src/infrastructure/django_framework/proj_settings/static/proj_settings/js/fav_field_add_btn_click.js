function favFieldAddBtnClick(url) {
    $.ajax({
        url: url,

        success: function(result) {
            window.location.href = window.location.href;
        },

        error: function(data) {
            alert('Failed to add new favourite config. Error: ' + data.responseText);
        }
    });
}