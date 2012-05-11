#set up the war
class War

  constructor: (opts) ->
    @user = opts.user
    @battleId = opts.battleId
    @userSocket = opts.userSocket
    @myTurn = opts.myTurn

    @map = opts.map
    @context = @map.canvas.getContext('2d')

    opts = {
      "user": @user,
      "battleId": @battleId+''
    }

    @sendData "ready", opts

  checkMouseDown: (e) ->
    if not @myTurn
      $('#notification').attr('class', 'alert')
      $('#notification').html("It's not your turn").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
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

        @sendData "attack",
          "coordinates": coordinates
          "battleId": @battleId
          "user": @user

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
      user: @user
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
      user: @user
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
      user: @user
      battleId: @battleId
      coordinates: coordinates

window.War = War