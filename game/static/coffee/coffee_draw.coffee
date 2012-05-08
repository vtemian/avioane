socket = io.connect("http://localhost:5555")
$(document).ready ->

  $("#submit").click ->

    username = $("#user").val()
    id = $('#id-user').val()
    battle = new Battle({
    'squareHeight': 30,
    'gameHolder': $('#gameHolder'),
    })

    $("#connection").html("waiting!")

    socket.emit "lobby-registration",
      username: username
      id: id

    socket.on "online", (data) ->
      online += 1
      $("#online").html(data)

    socket.on "start-battle", (data) ->
      $("#game").css("display", "block");
      battle.init()

    $("#start").click ->
      socket.emit "new-battle",
        firstUser: 0
        secondUser: 1
        battleId: 0

    $("#ready").click ->
      checked = battle.checkReady()
      if checked
        war = new War({
          'user': 0,
          'battleID': 0
          'userSocket': socket,
          'mapCanvas': checked
        })
