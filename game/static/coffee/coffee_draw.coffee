socket = io.connect("192.168.0.168:5555")

battle = ""

war = ""
weapons = {}
enemy = ""
myTurn = false
ready = 0
timer = ""
move_timer = ""
checked = false

class User
  constructor: (@username, @avion, @id) ->

class Countdown
  constructor: (@target_id, @start_time, @finished) ->
    @target_id = $('#seconds')
  init: ->
    @reset()
    window.tick = =>
      @tick()
    @my_interval = setInterval(window.tick, 1000)

  reset: ->
    #time = @start_time
    @seconds = parseInt(@start_time)
    @updateTarget()

  tick: ->

    [seconds] = [@seconds]
    if seconds > 0
      $('#timer>h1').remove()
      $('#timer>h2').remove()

      if seconds <= 10
        $('#timer').prepend('<h2>Hurry up!</h2>')
#        @seconds = seconds - 1
      else
        $('#timer').prepend('<h1>Your turn!</h1>')
#        @seconds = seconds - 1

    @updateTarget()
    if seconds is 1
      clearInterval(@my_interval)
      @finished()

  updateTarget: ->
    seconds = @seconds
    seconds = '0' + seconds if seconds < 10
    @target_id.html(seconds)

  clearMyInterval: ->
    $('#timer>h1').remove()
    $('#timer>h2').remove()
    $('#timer').prepend('<h2>Opponent!</h2>')
    @target_id.html('00')
    clearInterval(@my_interval);


class Users
  constructor: ->
    @dudes = {}

  add: (user) ->
    if @dudes.hasOwnProperty(user.id) == false
      @dudes[user.id] = user
      htmlToApend = '<li data-id="'+user.id+'"><h2 class=sty"online_player_name"><h2 class="online_player_name"><a class="online_player_link">'+user.username+'</a></h2><div class="online_player_plane"><img src="/static/img/user/lobby/avioane/'+user.avion+'.png" alt="'+user.avion+'" /></div><h3 class="online_player_battle"><a data-id="'+user.id+'">battle</a></h3></li>'
      $('#online_players_list').append(htmlToApend).hide().fadeIn(500);

  remove: (id) ->
    delete @dudes[id]
    $("li:[data-id = '"+id+"']").remove()

dude = new Users()

$(document).ready ->
  battleId = 0

  socket.emit "handshake",
    username: username,
    id: id,
    avion: avion

  socket.on "list", (data) ->
    user = new User(data.username, data.avion, data.id)
    dude.add(user)

  socket.on "remove-online", (id) ->
    dude.remove(id)

  $("#user_battle_button").click ->
    socket.emit "lobby-registration",
      username: username
      id: id

  socket.on "registration-complete", (data) ->
    $.post '/lobby/join/', (data) ->
      obj = $.parseJSON data
      if obj.not == "waiting"
        #waiting for player
        $('#notificationBig').html("Setting up battle...").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
        $('#notificationBig').attr('class', 'info notification')
        myTurn = true
      else
        if obj.not == "not-ready"
          $('#notificationBig').html("Sorry, but the players are in battle!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
          $('#notificationBig').attr('class', 'info notification')
        else
          #go to battle
          battleId = obj.battle


  socket.on "start-battle", (data) ->
    battle = new Battle({
    'squareHeight': 60,
    'gameHolder': $('#map'),
    })
    ready = 0
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
      $('#sub_header_holder').remove()

      $('#versus').css('display', 'block')

      setTimeout(
        ->
          $('#versus').fadeOut('slow', ->
              $("#battle").fadeIn(500).css('display', 'block')
              $("#start_battle_button").fadeIn(500).css('display', 'block')
#              get weapons
              $('#chat').css('display', 'block')
              $.get('/hangar/get-wepons/',
                (data) ->
                  obj = $.parseJSON(data)
                  $.each(obj.weapons, (index, item) ->
                    weapons[item.name] = item
                    $('#weapons-ul').append('<li data-type="'+item.name+'"><img src="/static/img/store/weapons/'+item.image+'.png" alt="radar"></li>')
                  )
                  console.log war.userWeapons
              )
              timer = new Countdown("#time_left", "60",
                ->
                  $.post('/battle/', {'state': 'loss', 'enemy': enemy, 'battleId': battleId},

                    ->
                      socket.emit "finish",
                        battleId: battleId
                        user: id

                      $('#notificationBig').attr('class', 'alert notification')
                      $('#notificationBig').html("You lost").dequeue().stop().slideDown(200).delay(1700).slideUp(200 ,-> window.location = '/')

                      myTurn = false

                  )


              )
              timer.init()


          )
        , 3000);


    )

    if data.firstUser == id
      enemy = data.secondUser
    else
      enemy = data.firstUser

  $('li[data-type=shield]').live("click", ->
      if checked
        if war.myTurn
          $('#notificationBig').attr('class', 'alert notification')
          $('#notificationSmall').html("Choose a position to defend").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
          war.weaponSet = 'shield'
        else
          $('#notificationBig').attr('class', 'alert notification')
          $('#notificationBig').html("Not your turn").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
      else
        $('#notificationBig').attr('class', 'info notification')
        $('#notificationBig').html("Start the battle first!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
  )
  socket.on "weapon-usage", (data) ->
    war.myTurn = true
    war.move_timer = new Countdown("#time_left", "30",
      ->
        war.sendData "next-turn",
          enemy: enemy

        $('#notificationSmall').attr('class', 'alert notification')
        $('#notificationSmall').html("To late!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
        war.move_timer.clearMyInterval()
        war.myTurn = false;
    )
    war.move_timer.init()

  socket.on "ready", (data) ->
    #check if i'm ready or my enemy
    if username != data
      ready += 1
      if war.ready != undefined
        war.ready = ready
      if ready == 2
        $('#notificationSmall').attr('class', 'succes notification')
        $('#notificationSmall').html("Start battle!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
        if war.myTurn
          war.move_timer = new Countdown("#time_left", "30",
            ->
              war.sendData "next-turn",
                enemy: enemy

              $('#notificationSmall').attr('class', 'alert notification')
              $('#notificationSmall').html("To late!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
              war.move_timer.clearMyInterval()
              war.myTurn = false
          )
          war.move_timer.init()
        else
          war.sendData "next-turn",
            enemy: enemy
      else
        $('#notificationSmall').attr('class', 'info notification')
        $('#notificationSmall').html("Your enemy is ready to play!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)

  socket.on "check-hit", (data) ->
    war.myTurn = true

    $('#notificationSmall').attr('class', 'succes notification')
    $('#notificationSmall').html("It's your turn!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
    war.move_timer = new Countdown("#time_left", "30",
      ->
        war.sendData "next-turn",
          enemy: enemy

        $('#notificationSmall').attr('class', 'alert notification')
        $('#notificationSmall').html("To late!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
        war.move_timer.clearMyInterval()
        war.myTurn = false;
    )
    war.move_timer.init()

    x = data.coordinates.x
    y = data.coordinates.y
    $.post('/battle/attack/', {'x': x, 'y': y, 'battleID': battleId}, (data) ->
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

              $('#notificationBig').attr('class', 'alert notification')
              $('#notificationBig').html("You lost").dequeue().stop().slideDown(200).delay(1700).slideUp(200, -> window.location = '/')

              war.myTurn = false

            )
          else
            war.head_attack x, y, 0, 60*11-25
    )

  socket.on "win", ->
    $('#notificationSmall').attr('class', 'succes notification')
    $('#notificationSmall').html("You won").dequeue().stop().slideDown(200).delay(1700).slideUp(200, -> window.location = '/')
    myTurn = false

  socket.on "miss", (data) ->
    x = data.coordinates.x
    y = data.coordinates.y
    war.draw_attack
      x: x * war.map.squareHeight + war.map.position.left
      y: y * war.map.squareHeight + war.map.position.top
      height: war.map.squareHeight
      fillStyle: "#f2e9e1"
    $('#notificationSmall').attr('class', 'alert notification')
    $('#notificationSmall').html("Miss!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)

  socket.on "hit", (data) ->
    x = data.coordinates.x
    y = data.coordinates.y
    war.draw_attack
      x: x * war.map.squareHeight + war.map.position.left
      y: y * war.map.squareHeight + war.map.position.top
      height: war.map.squareHeight
      fillStyle: "#f8ca00"
    $('#notificationSmall').attr('class', 'info notification')
    $('#notificationSmall').html("Hit!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)

  socket.on "head", (data) ->
    x = data.coordinates.x
    y = data.coordinates.y
    war.draw_attack
      x: x * war.map.squareHeight + war.map.position.left
      y: y * war.map.squareHeight + war.map.position.top
      height: war.map.squareHeight
      fillStyle: "#fa2a00"
    $('#notificationSmall').attr('class', 'succes notification')
    $('#notificationSmall').html("OMG a head!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)

  socket.on "next-turn", (data) ->
    war.myTurn = true
    $('#notificationSmall').attr('class', 'succes notification')
    $('#notificationSmall').html("It's your turn!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
    war.move_timer = new Countdown("#time_left", "30",
      ->
        war.sendData "next-turn",
          enemy: enemy

        $('#notificationSmall').attr('class', 'alert notification')
        $('#notificationSmall').html("To late!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
        war.move_timer.clearMyInterval()
        war.myTurn = false;
    )
    war.move_timer.init()

  socket.on "disconnectGame", (data) ->
    $.post('/battle/disconnect/', {'enemy': enemy, 'battleID': battleId, "state":"loss"}, ->
      $('#notificationBig').attr('class', 'succes notification')
      $('#notificationBig').html("You won").dequeue().stop().slideDown(200).delay(1700).slideUp(200, -> window.location = '/')
    )
    myTurn = false

  socket.on "receive-invitation", (data) ->
    $('#notificationBig').attr('class', 'alert notification')
    html = "<div id='invitation-notification' data-id='" + data.id + "' >" + data.username + " wants to battle you! Do you accept the battle? <a id='accept-invitation' class='button'>Yes</a> or <a class='button'>No</a></div>"
    $('#notificationBig').html(html).dequeue().stop().slideDown(200)

  $("#accept-invitation").live "click", ->
    id = $(this).parent().data('id')
    $.get('battle/accept-invitation/', { userid:id }, (data)->
    )
    $(this).parent().parent().slideUp(200);
    myTurn = true

  $("#start_battle_button").click ->
    checked = battle.checkReady(battleId)
    if checked
      $("#start_battle_button").remove()
      timer.clearMyInterval()
      ready += 1
      console.log weapons
      war = new War({
        'user': id,
        'enemy': enemy,
        'battleId': battleId
        'userSocket': socket,
        'map': checked,
        'myTurn': myTurn,
        'ready': ready,
        'move_timer': move_timer,
        'weapons': weapons
      })
      war.map.canvas.onmousedown = (e) ->
        war.checkMouseDown e

  $("li:[data-id]").live "click", (e) ->
    id = $(this).data("id")
    $.post("/battle/send-invitation/", {toUserId: id}, (data) ->
      if data == 'not-ready'
        $('#notificationBig').attr('class', 'alert notification')
        $('#notificationBig').html("You can't invite him right now! He is already invited!").dequeue().stop().slideDown(200).delay(2000).slideUp(200)
      else
        if data == 'battle'
          $('#notificationBig').attr('class', 'alert notification')
          $('#notificationBig').html("Your buddy is in a battle! Wait for him to finish!").dequeue().stop().slideDown(200).delay(2000).slideUp(200)
        else
          $('#notificationBig').attr('class', 'info notification')
          $('#notificationBig').html("Ready for battle!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
    )
    myTurn = false

  socket.on "chat", (data) ->
    $("#chat_middle").prepend('<p class="chat_opponent"><b>Enemy:</b>'+data+'</p>')

  $("#chat-text").bind('keypress', (e) ->
    if(e.keyCode==13)
      e.preventDefault()
      str = $(this).val()
      str=str.replace(/\\/g,'\\\\');
      str=str.replace(/\'/g,'\\\'');
      str=str.replace(/\"/g,'\\"');
      str=str.replace(/\0/g,'\\0');
      $(this).val(" ")
      socket.emit "chat", {'enemy': enemy, 'message': str}
      $("#chat_middle").prepend('<p class="chat_you"><b>You:</b>'+str+'</p>')
  )
