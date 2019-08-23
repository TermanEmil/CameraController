function hardResetBtnClick(button, url) {

    button.disabled = true;

    spinner = button.getElementsByClassName('spinner')[0];
    spinner.hidden = false;

    $.ajax({
        url: url,

        success: function() {
            location.reload();
        },

        error: function(data) {
            alert('Failed to hard reset ports. Error: ' + data.responseText);
        }
    }).always(function() {
        button.disabled = false;
        spinner.hidden = true;
    });
}