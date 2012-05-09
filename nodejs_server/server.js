// Generated by CoffeeScript 1.3.1
(function() {
  var Battle, Battles, Clients, User, battles, io, lobby, online, online_peoples;

  io = require('socket.io').listen(5555);

  Clients = (function() {

    Clients.name = 'Clients';

    function Clients() {
      this.clients = {};
      this.users = {};
      this.length = 0;
    }

    Clients.prototype.add = function(client) {
      if (this.clients[client.socket.id] === void 0) {
        console.log('New player', client.username, client.socket.id);
        this.clients[client.socket.id] = client;
        this.users[client.id] = client;
        return this.length++;
      }
    };

    Clients.prototype.remove = function(socket) {
      delete this.clients[socket.id];
      return this.length--;
    };

    Clients.prototype.get = function(socket) {
      return this.clients[socket.id];
    };

    Clients.prototype.getById = function(id) {
      var client, idClient, _ref;
      _ref = this.clients;
      for (idClient in _ref) {
        client = _ref[idClient];
        if (client.id === id) {
          return client;
        }
      }
    };

    Clients.prototype.broadcast = function(event, data) {
      var client, id, _ref, _results;
      _ref = this.clients;
      _results = [];
      for (id in _ref) {
        client = _ref[id];
        _results.push(client.socket.emit(event, data));
      }
      return _results;
    };

    return Clients;

  })();

  User = (function() {

    User.name = 'User';

    function User(opts) {
      this.username = opts.username;
      this.socket = opts.socket;
      this.id = opts.id;
      this.avion = opts.avion;
      this.ready = false;
    }

    return User;

  })();

  Battle = (function() {

    Battle.name = 'Battle';

    function Battle(firstUser, secondUser, battleId) {
      this.firstUser = firstUser;
      this.secondUser = secondUser;
      this.battleId = battleId;
    }

    Battle.prototype.start = function() {
      return this.emit("start-battle", {
        firstUser: this.firstUser.username,
        secondUser: this.secondUser.username,
        battleId: this.battleId
      });
    };

    Battle.prototype.emit = function(event, message) {
      this.firstUser.socket.emit(event, message);
      return this.secondUser.socket.emit(event, message);
    };

    Battle.prototype.attacking_moves = function(user, coordinates, event) {
      user = lobby.getById(user);
      if (user === this.firstUser) {
        return this.secondUser.socket.emit(event, {
          coordinates: coordinates
        });
      } else {
        return this.firstUser.socket.emit(event, {
          coordinates: coordinates
        });
      }
    };

    Battle.prototype.ready = function(user) {
      user = lobby.getById(user);
      user.ready = true;
      return this.emit("ready", user.username);
    };

    Battle.prototype.finish = function(user) {
      user = lobby.getById(user);
      if (user === this.firstUser) {
        return this.secondUser.socket.emit("win");
      } else {
        return this.firstUser.socket.emit("win");
      }
    };

    return Battle;

  })();

  Battles = (function() {

    Battles.name = 'Battles';

    function Battles() {
      this.battles = {};
    }

    Battles.prototype.add = function(battle) {
      this.battles[battle.battleId] = battle;
      return console.log("new battle in town!", battle);
    };

    Battles.prototype.remove = function(battle) {
      return delete this.battles[battle.id];
    };

    Battles.prototype.get = function(id) {
      return this.battles[id];
    };

    return Battles;

  })();

  lobby = new Clients();

  online = new Clients();

  battles = new Battles();

  online_peoples = 0;

  io.sockets.on('connection', function(socket) {
    online_peoples += 1;
    socket.emit("online-peoples", online_peoples);
    socket.broadcast.emit("online-peoples", online_peoples);
    socket.on('handshake', function(data) {
      var client, idClient, newUser, _ref;
      newUser = new User({
        username: data.username,
        id: data.id,
        socket: socket,
        avion: data.avion
      });
      _ref = online.clients;
      for (idClient in _ref) {
        client = _ref[idClient];
        socket.emit("list", {
          'username': client.username,
          'id': client.id,
          'avion': client.avion
        });
      }
      online.add(newUser);
      return online.broadcast('list', {
        'username': newUser.username,
        'id': newUser.id,
        'avion': newUser.avion
      });
    });
    socket.on('lobby-registration', function(data) {
      var newUser;
      newUser = new User({
        username: data.username,
        socket: socket,
        id: data.id
      });
      lobby.add(newUser);
      lobby.broadcast('online', lobby.length);
      return socket.emit("registration-complete");
    });
    socket.on('new-battle', function(data) {
      var battle, firstUser, secondUser;
      firstUser = lobby.getById(data.firstUser);
      secondUser = lobby.getById(data.secondUser);
      battle = new Battle(firstUser, secondUser, data.battleId);
      battles.add(battle);
      return battle.start();
    });
    socket.on("ready", function(data) {
      var battle;
      battle = battles.get(data.battleId);
      return battle.ready(data.user);
    });
    socket.on("attack", function(data) {
      var battle;
      battle = battles.get(data.battleId);
      return battle.attacking_moves(data.user, data.coordinates, "check-hit");
    });
    socket.on("miss-attack", function(data) {
      var battle;
      battle = battles.get(data.battleId);
      return battle.attacking_moves(data.user, data.coordinates, "miss");
    });
    socket.on("hit-attack", function(data) {
      var battle;
      battle = battles.get(data.battleId);
      return battle.attacking_moves(data.user, data.coordinates, "hit");
    });
    socket.on("head-attack", function(data) {
      var battle;
      battle = battles.get(data.battleId);
      return battle.attacking_moves(data.user, data.coordinates, "head");
    });
    socket.on("finish", function(data) {
      var battle;
      battle = battles.get(data.battleId);
      battle.finish(data.user);
      return battles.remove(battle);
    });
    socket.on("send-invitation", function(data) {
      var fromUser, toUser;
      fromUser = online.getById(data.fromUser);
      toUser = online.getById(data.toUser);
      return toUser.socket.emit("receive-invitation", {
        username: fromUser.username,
        id: fromUser.id
      });
    });
    socket.on('test', function(data) {
      return console.log(data);
    });
    return socket.on('disconnect', function() {
      var battle, battleid, client, _ref;
      online_peoples -= 1;
      socket.broadcast.emit("online-peoples", online_peoples);
      client = lobby.get(socket);
      if (client !== void 0) {
        _ref = battles.battles;
        for (battleid in _ref) {
          battle = _ref[battleid];
          if (battle.firstUser.username === client.username) {
            battle.secondUser.socket.emit("disconnectGame");
          } else {
            if (battle.secondUser.username === client.username) {
              battle.firstUser.socket.emit("disconnectGame");
            }
          }
        }
        console.log(client);
      }
      lobby.remove(socket);
      client = online.get(socket);
      if (client !== void 0) {
        online.remove(socket);
        return online.broadcast("remove-online", client.id);
      }
    });
  });

}).call(this);
