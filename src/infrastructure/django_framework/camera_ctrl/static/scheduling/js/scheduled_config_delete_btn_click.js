function scheduledConfigDeleteBtnClick(url) {
    $.ajax({
        url: url,

        success: function() {
            window.location.href = $("#list-url").val();
        },

        error: function(data) {
            alert('Failed to delete scheduled config. Error: ' + data.responseText);
        }
    });
}