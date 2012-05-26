#set up the war
class War

  constructor: (opts) ->
    @user = opts.user
    @enemy = opts.enemy
    @battleId = opts.battleId
    @userSocket = opts.userSocket
    @myTurn = opts.myTurn
    @ready = opts.ready
    @move_timer = opts.move_timer

    @shieldTurn = false

    @map = opts.map
    @context = @map.canvas.getContext('2d')

    opts = {
      "user": @user,
      "battleId": @battleId+''
    }

    @sendData "ready", opts

  checkMouseDown: (e) ->
    if @ready < 2
      $('#notificationSmall').attr('class', 'info notification')
      $('#notificationSmall').html("Your enemy it's not ready!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
    else
      if not @myTurn
        $('#notificationSmall').attr('class', 'alert notification')
        $('#notificationSmall').html("It's not your turn").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
      else
          squareHeight = @map.squareHeight
          position = @map.position

          maxTop = position.top + squareHeight * 10
          maxLeft = position.left + squareHeight * 10

          top = e.offsetY
          left = e.offsetX

          if top < maxTop and top > position.top and left < maxLeft and left > position.left
            y = parseInt((top-position.top) / squareHeight)
            x = parseInt((left-position.left) / squareHeight)
            coordinates = {
              "x": x,
              "y": y
            }
            @move_timer.clearMyInterval()
            @sendData "attack",
              "coordinates": coordinates
              "battleId": @battleId
              "user": @enemy

            @myTurn = false

  sendData: (event, message) ->
    @userSocket.emit event, message

  draw_attack: (opts) ->
    @context.fillStyle = opts.fillStyle

    @context.beginPath()
    @context.rect opts.x, opts.y, opts.height, opts.height
    @context.fill()
    @context.stroke()

  miss_attack: (x, y, left, top) ->

    @draw_attack
      x: x * 27 + top
      y: y * 27 + left
      height: 27
      fillStyle: "#FFF"

    coordinates =
      x: x
      y: y

    @sendData "miss-attack",
      user: @enemy
      battleId: @battleId
      x: x
      y: y
      coordinates: coordinates


  hit_attack: (x, y, left, top) ->

    @draw_attack
      x: x * 27 + top
      y: y * 27 + left
      height: 27
      fillStyle: "blue"

    coordinates =
      x: x
      y: y

    @sendData "hit-attack",
      user: @enemy
      battleId: @battleId
      x: x
      y: y
      coordinates: coordinates

  head_attack: (x, y, left, top) ->
    @draw_attack
      x: x * 27 + top
      y: y * 27 + left
      height: 27
      fillStyle: "yellow"

    coordinates =
      x: x
      y: y

    @sendData "head-attack",
      user: @enemy
      battleId: @battleId
      coordinates: coordinates

window.War = War