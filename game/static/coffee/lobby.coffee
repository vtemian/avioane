$(document).ready ->
  $('#user_level_bar_progress').css('width', parseInt(progress)+'%')
  $('#user_progress').html(parseInt(progress))