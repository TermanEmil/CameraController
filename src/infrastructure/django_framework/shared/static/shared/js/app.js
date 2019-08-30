$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

$(document).ready(function(){
  $('.toast').toast('show');
  $('.toast').attr("hidden", false);
});

// 0 padded number
function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}