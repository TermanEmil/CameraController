function camerasAutodetectBtnClick(button, url) {
    button.disabled = true;

    spinner = button.getElementsByClassName('spinner')[0];
    spinner.hidden = false;

    $.ajax({
        url: url,

        success: function() {
            location.reload();
        },

        error: function(data) {
            alert('Failed to detect cameras. Error: ' + data.responseText);
        }
    }).always(function() {
        button.disabled = false;
        spinner.hidden = true;
    });
}