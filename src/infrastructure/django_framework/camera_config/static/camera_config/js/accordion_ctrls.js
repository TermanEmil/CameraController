$('.closeall').click(function() {
  $('.panel-collapse.show')
    .collapse('hide');
});

$('.openall').click(function(){
  $('.panel-collapse:not(".in")')
    .collapse('show');
});