function timelapseDeleteBtnClick(url) {
    console.log(url);
    $.ajax({
        url: url,

        success: function() {
            window.location.href = $("#list-url").val();
        },

        error: function(data) {
            alert('Failed to delete timelapse. Error: ' + data.responseText);
        }
    });
}