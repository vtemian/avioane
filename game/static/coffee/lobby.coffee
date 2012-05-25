$(document).ready ->
  $('#user_level_bar_fluid').css('width', parseInt(progress)+'%')
  $('#user_level_progress').html(parseInt(progress)+'%')

  $('#user_division_bar').css('width', parseInt(division_progress)+'%')


  $('#user_hangar_button').click ->
    window.location = '/hangar'

  $("#user_profile").click ->
    window.location = '/profile/' + $(this).data('id')
