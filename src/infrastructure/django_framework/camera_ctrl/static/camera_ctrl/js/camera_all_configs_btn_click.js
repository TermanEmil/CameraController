function cameraAllConfigsBtnClick(element) {
    var iconElement = element.getElementsByTagName("i")[0];

    iconElement.className = "fa fa-fw fa-spinner fa-spin";
    element.onclick = function(event) {
        event.preventDefault();
    }
}