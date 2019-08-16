function scheduleDeleteBtnClick(url) {


    $.ajax({
        url: url,

        success: function() {
            window.location.href = $("#list-url").val();
        },

        error: function(data) {
            alert('Failed to delete schedule. Error: ' + data.responseText);
        }
    });
}