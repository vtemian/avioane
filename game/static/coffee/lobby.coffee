$(document).ready ->
  $('#user_level_bar_fluid').css('width', parseInt(progress)+'%')
  $('#user_level_progress').html(parseInt(progress)+'%')