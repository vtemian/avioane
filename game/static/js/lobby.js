// Generated by CoffeeScript 1.3.3
(function() {

  $(document).ready(function() {
    $('#user_level_bar_fluid').css('width', parseInt(progress) + '%');
    $('#user_level_progress').html(parseInt(progress) + '%');
    $('#user_division_bar').css('width', parseInt(division_progress) + '%');
    $('#user_hangar_button').click(function() {
      return window.location = '/hangar';
    });
    return $("#user_profile").click(function() {
      return window.location = '/profile/' + $(this).data('id');
    });
  });

}).call(this);
