socket = io.connect("http://outclan.com:5555")

battleId = 0
war = ""
enemy = ""
myTurn = false


class User
  constructor: (@username, @avion, @id) ->

class Users
  constructor: ->
    @dudes = {}

  add: (user) ->
    if @dudes.hasOwnProperty(user.id) == false
      @dudes[user.id] = user
      htmlToApend = '<li data-id="'+user.id+'"><h2 class="online_player_name"><h2 class="online_player_name"><a class="online_player_link">'+user.username+'</a></h2><div class="online_player_plane"><img src="/static/img/user/lobby/avioane/'+user.avion+'.png" alt="'+user.avion+'" /></div><h3 class="online_player_battle"><a data-id="'+user.id+'">battle</a></h3></li>'
      $('#online_players_list').append(htmlToApend).hide().fadeIn(500);

  remove: (id) ->
    delete @dudes[id]
    $("li:[data-id = '"+id+"']").remove()

dude = new Users()

$(document).ready ->

  socket.emit "handshake",
    username: username,
    id: id,
    avion: avion

  socket.on "list", (data) ->
    user = new User(data.username, data.avion, data.id)
    dude.add(user)

  socket.on "remove-online", (id) ->
    console.log id
    dude.remove(id)

  socket.on "online", (data) ->
    online += 1
    $("#online").html(data)

  $("#user_battle").click ->
    socket.emit "lobby-registration",
      username: username
      id: id

  socket.on "registration-complete", (data) ->
    $.post '/lobby/join/', (data) ->
      obj = $.parseJSON data
      if obj.not != undefined
        #waiting for player
        $('#notification').html("Setting up battle...").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
        $('#notification').attr('class', 'info')
        myTurn = true
      else
        #go to battle
        battleId = obj.battle


  socket.on "start-battle", (data) ->
    battle = new Battle({
    'squareHeight': 60,
    'gameHolder': $('#map'),
    })

    battle.init()

    battleId = data.battleId
    $.get( '/battle/get-details/', {'battleId': battleId}, (data) ->
      obj = $.parseJSON data
      user1 = obj.user1
      user2 = obj.user2
      $('#lvl1').html("level: " + user1.lvl)
      $('#lvl2').html("level: " + user2.lvl)

      $('#won1').html("won: " + user1.won)
      $('#won2').html("won: " + user2.won)

      $('#lost1').html("lost: " + user1.lost)
      $('#lost2').html("lost: " + user2.lost)

      $('#img1').attr('src', "/static/img/user/lobby/avioane/"+user1.avion+".png")
      $('#img2').attr('src', "/static/img/user/lobby/avioane/"+user2.avion+".png")

      $('#versus_p1_name').html(user1.username)
      $('#versus_p2_name').html(user2.username)

      $('#sub_holder').remove()
      $('#lobby').remove()

      $('#versus').css('display', 'block')

      setTimeout(
        ->
          $('#versus').fadeOut('slow', ->
              $("#battle").fadeIn(500).css('display', 'block')
              $("#start_battle_button").fadeIn(500).css('display', 'block')
          )
        , 3000);
    )

    if data.firstUser == id
      enemy = data.secondUser
    else
      enemy = data.firstUser

  socket.on "ready", (data) ->
    #check if i'm ready or my enemy
    if username != data
      console.log "your enemy is ready"

  socket.on "check-hit", (data) ->
    war.myTurn = true
    x = data.coordinates.x
    y = data.coordinates.y
    $.post('/battle/attack/', {'x': x, 'y': y, 'battleID': battleId}, (data) ->
      console.log data
      if data == 'miss'
        war.miss_attack x, y, 0, 60*11-25
      else
        if data == 'hit'
          war.hit_attack x, y, 0, 60*11-25
        else
          if data == 'finished'
            $.post('/battle/', {'state': 'loss', 'enemy': enemy, 'battleId': battleId}, (data) ->

              socket.emit "finish",
                battleId: battleId
                user: id

              $('#notification').attr('class', 'alert')
              $('#notification').html("You lost").dequeue().stop().slideDown(200).delay(1700).slideUp(200 ,-> window.location = '/')
            )
          else
            war.head_attack x, y, 0, 60*11-25
    )

  socket.on "win", ->
    $('#notification').attr('class', 'succes')
    $('#notification').html("You won").dequeue().stop().slideDown(200).delay(1700).slideUp(200 ,-> window.location = '/')
  socket.on "miss", (data) ->

    x = data.coordinates.x
    y = data.coordinates.y
    war.draw_attack
      x: x * war.map.squareHeight + war.map.position.left
      y: y * war.map.squareHeight + war.map.position.top
      height: war.map.squareHeight
      fillStyle: "#FFF"
    console.log "miss"

  socket.on "hit", (data) ->
    x = data.coordinates.x
    y = data.coordinates.y
    war.draw_attack
      x: x * war.map.squareHeight + war.map.position.left
      y: y * war.map.squareHeight + war.map.position.top
      height: war.map.squareHeight
      fillStyle: "blue"
    console.log "hit"

  socket.on "head", (data) ->
    x = data.coordinates.x
    y = data.coordinates.y
    war.draw_attack
      x: x * war.map.squareHeight + war.map.position.left
      y: y * war.map.squareHeight + war.map.position.top
      height: war.map.squareHeight
      fillStyle: "yellow"
    console.log "head"

  socket.on "disconnectGame", (data) ->
    $.post('/battle/disconnect/', {'enemy': enemy, 'battleID': battleId}, ->
      $('#notification').attr('class', 'succes')
      $('#notification').html("You won").dequeue().stop().slideDown(200).delay(1700).slideUp(200 ,-> window.location = '/')
    )

  socket.on "receive-invitation", (data) ->
    console.log data
    console.log "aasdasdadasdasdad"
    $('#notification').attr('class', 'succes')
    html = "<div id='invitation-notification' data-id='" + data.id + "'>" + data.username + " invited you to play! <button id='accept-invitation'>Accept</button><button id='decline-invitation'>Decline</button></div>"
    $('#notification').html(html).dequeue().stop().slideDown(200)

  $("#accept-invitation").live "click", ->
    id = $(this).parent().data('id')
    $.get('battle/accept-invitation/', ->

    )
    $(this).parent().parent().slideUp(200);

  $("#start_battle_button").click ->

    checked = battle.checkReady(battleId)
    if checked
      $("#start_battle_button").remove()
      war = new War({
        'user': enemy,
        'battleId': battleId
        'userSocket': socket,
        'map': checked,
        'myTurn': myTurn
      })
      war.map.canvas.onmousedown = (e) ->
        war.checkMouseDown e

  $("li:[data-id]").live "click", (e) ->
    id = $(this).data("id")
    $.post("/battle/send-invitation/", {toUserId: id}, (data) ->
      console.log data
    )
