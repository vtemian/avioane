
io = require('socket.io').listen(5555)

class Clients
  constructor: ->
    @clients = {}
    @users = {}
    @length = 0

  add: (client) ->
      if @clients[client.socket.id] == undefined
        console.log 'New player', client.username, client.socket.id
        @clients[client.socket.id] = client
        @users[client.id] = client
        @length++

  remove: (socket) ->
    delete @clients[socket.id]
    @length--

  get: (socket) ->
    return @clients[socket.id]

  getById: (id) ->
    for idClient, client of @clients
      if client.id == id
        return client

  broadcast: (event, data) ->
    for id, client of @clients
      client.socket.emit event, data

class User
  constructor: (opts)->
    @username = opts.username
    @socket = opts.socket
    @id = opts.id
    @avion = opts.avion

    @ready = false

class Battle
  constructor: (@firstUser, @secondUser, @battleId) ->

  start: ->
    @emit "start-battle",
      firstUser: @firstUser.id
      secondUser: @secondUser.id
      battleId: @battleId

  emit: (event, message) ->
    @firstUser.socket.emit event, message
    @secondUser.socket.emit event, message

  attacking_moves: (user, coordinates, event) ->
    user = lobby.getById user
    @user.socket.emit event,
      coordinates: coordinates

  ready: (user) ->
    user = lobby.getById user
    user.ready = true
    @emit "ready",
      user.username

  finish: (user) ->
    user = lobby.getById user
    if user == @firstUser
      @secondUser.socket.emit "win"
    else
      @firstUser.socket.emit "win"

class Battles
  constructor: () ->
    @battles = {}

  add: (battle) ->
    @battles[battle.battleId] = battle
    console.log "new battle in town!", battle

  remove: (battle) ->
    delete @battles[battle.id]

  get: (id) ->
    return @battles[id]

lobby = new Clients()
online = new Clients()

battles = new Battles()

online_peoples = 0

io.sockets.on 'connection', (socket) ->
  online_peoples += 1
  socket.emit "online-peoples", online_peoples
  socket.broadcast.emit "online-peoples", online_peoples


  socket.on 'handshake', (data) ->
    newUser = new User
      username: data.username
      id: data.id
      socket: socket
      avion: data.avion

    for idClient, client of online.clients
      socket.emit "list", {
        'username':client.username,
        'id': client.id,
        'avion': client.avion
      }
    online.add newUser

    online.broadcast 'list', {
      'username': newUser.username,
      'id': newUser.id,
      'avion': newUser.avion
    }



  socket.on 'lobby-registration', (data) ->
    newUser = new User
      username: data.username
      socket: socket
      id: data.id

    lobby.add newUser
    lobby.broadcast 'online', lobby.length

    socket.emit "registration-complete"

  socket.on 'new-battle', (data) ->
    firstUser = online.getById data.firstUser
    secondUser = online.getById data.secondUser
    battle = new Battle firstUser, secondUser, data.battleId
    battles.add battle
    battle.start()

  socket.on "ready", (data) ->
    battle = battles.get(data.battleId)
    #ready a player
    battle.ready(data.user)

  socket.on "attack", (data) ->
    battle = battles.get(data.battleId)
    battle.attacking_moves data.user, data.coordinates, "check-hit"

  socket.on "miss-attack", (data) ->
    battle = battles.get(data.battleId)
    battle.attacking_moves data.user, data.coordinates, "miss"

  socket.on "hit-attack", (data) ->
    battle = battles.get(data.battleId)
    battle.attacking_moves data.user, data.coordinates, "hit"

  socket.on "head-attack", (data) ->
    battle = battles.get(data.battleId)
    battle.attacking_moves data.user, data.coordinates, "head"

  socket.on "finish", (data) ->
    battle = battles.get(data.battleId)
    battle.finish data.user
    battles.remove battle

  socket.on "send-invitation", (data) ->
    fromUser = online.getById data.fromUser
    toUser = online.getById data.toUser
    console.log data
    toUser.socket.emit "receive-invitation",
      username: fromUser.username
      id: fromUser.id

  socket.on 'test', (data) ->
    console.log data

  socket.on 'disconnect', ->
    online_peoples -= 1
    socket.broadcast.emit "online-peoples", online_peoples

    client = online.get socket

    if client != undefined
      for battleid,battle of battles.battles
        if battle.firstUser.username == client.username
          battle.secondUser.socket.emit "disconnectGame"
        else
            if battle.secondUser.username == client.username
              battle.firstUser.socket.emit "disconnectGame"
      console.log client

    lobby.remove socket



    if client != undefined
      online.remove socket
      online.broadcast "remove-online", client.id

