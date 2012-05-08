
io = require('socket.io').listen(5555)

class Clients
  constructor: ->
    @clients = {}
    @length = 0

  add: (client) ->
    console.log 'New player', client.username, client.socket.id
    @clients[client.socket.id] = client
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

class Battle
  constructor: (@firstUser, @secondUser, @battleId) ->

  start: ->
    @emit "start-battle",
      firstUser: @firstUser.username
      secondUser: @secondUser.username

  emit: (event, message) ->
    @firstUser.socket.emit event, message
    @secondUser.socket.emit event, message

class Battles
  constructor: () ->
    @battles = {}

  add: (battle) ->
    @battles[battle.id] = battle
    console.log "new battle in town!", battle

  remove: (battle) ->
    delete @battles[battle.id]

  get: (id) ->
    return @battles[id]

lobby = new Clients()
battles = new Battles()

io.sockets.on 'connection', (socket) ->

  socket.on 'lobby-registration', (data) ->
    newUser = new User
      username: data.username
      socket: socket
      id: (Number) data.id

    lobby.add newUser
    lobby.broadcast 'online', lobby.length


  socket.on 'new-battle', (data) ->
    firstUser = lobby.getById data.firstUser
    secondUser = lobby.getById data.secondUser
    battle = new Battle firstUser, secondUser, data.battleId
    battles.add battle
    battle.start()

  socket.on 'test', (data) ->
    console.log data

  socket.on 'disconnect', ->
    lobby.remove socket
