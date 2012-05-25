// Generated by CoffeeScript 1.3.1
(function() {
  var Countdown, User, Users, battle, dude, enemy, move_timer, myTurn, ready, socket, timer, war;

  socket = io.connect("http://outclan.com:5555");

  battle = "";

  war = "";

  enemy = "";

  myTurn = false;

  ready = 0;

  timer = "";

  move_timer = "";

  User = (function() {

    User.name = 'User';

    function User(username, avion, id) {
      this.username = username;
      this.avion = avion;
      this.id = id;
    }

    return User;

  })();

  Countdown = (function() {

    Countdown.name = 'Countdown';

    function Countdown(target_id, start_time, finished) {
      this.target_id = target_id;
      this.start_time = start_time;
      this.finished = finished;
    }

    Countdown.prototype.init = function() {
      var _this = this;
      this.reset();
      window.tick = function() {
        return _this.tick();
      };
      return this.my_interval = setInterval(window.tick, 1000);
    };

    Countdown.prototype.reset = function() {
      this.seconds = parseInt(this.start_time);
      return this.updateTarget();
    };

    Countdown.prototype.tick = function() {
      var seconds;
      seconds = [this.seconds][0];
      if (seconds > 0) {
        if (seconds === 10) {
          console.log("WARNING! You have 10 secnds left");
          this.seconds = seconds - 1;
        } else {
          this.seconds = seconds - 1;
        }
      }
      this.updateTarget();
      if (seconds === 1) {
        clearInterval(this.my_interval);
        return this.finished();
      }
    };

    Countdown.prototype.updateTarget = function() {
      var seconds;
      seconds = this.seconds;
      if (seconds < 10) {
        seconds = '0' + seconds;
      }
      return console.log("Seconds left:" + seconds);
    };

    Countdown.prototype.clearMyInterval = function() {
      return clearInterval(this.my_interval);
    };

    return Countdown;

  })();

  Users = (function() {

    Users.name = 'Users';

    function Users() {
      this.dudes = {};
    }

    Users.prototype.add = function(user) {
      var htmlToApend;
      if (this.dudes.hasOwnProperty(user.id) === false) {
        this.dudes[user.id] = user;
        htmlToApend = '<li data-id="' + user.id + '"><h2 class=sty"online_player_name"><h2 class="online_player_name"><a class="online_player_link">' + user.username + '</a></h2><div class="online_player_plane"><img src="/static/img/user/lobby/avioane/' + user.avion + '.png" alt="' + user.avion + '" /></div><h3 class="online_player_battle"><a data-id="' + user.id + '">battle</a></h3></li>';
        return $('#online_players_list').append(htmlToApend).hide().fadeIn(500);
      }
    };

    Users.prototype.remove = function(id) {
      delete this.dudes[id];
      return $("li:[data-id = '" + id + "']").remove();
    };

    return Users;

  })();

  dude = new Users();

  $(document).ready(function() {
    var battleId;
    battleId = 0;
    socket.emit("handshake", {
      username: username,
      id: id,
      avion: avion
    });
    socket.on("list", function(data) {
      var user;
      user = new User(data.username, data.avion, data.id);
      return dude.add(user);
    });
    socket.on("remove-online", function(id) {
      return dude.remove(id);
    });
    $("#user_battle_button").click(function() {
      return socket.emit("lobby-registration", {
        username: username,
        id: id
      });
    });
    socket.on("registration-complete", function(data) {
      return $.post('/lobby/join/', function(data) {
        var obj;
        obj = $.parseJSON(data);
        if (obj.not === "waiting") {
          $('#notificationBig').html("Setting up battle...").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
          $('#notificationBig').attr('class', 'info notification');
          return myTurn = true;
        } else {
          if (obj.not === "not-ready") {
            $('#notificationBig').html("Sorry, but the players are in battle!").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
            return $('#notificationBig').attr('class', 'info notification');
          } else {
            return battleId = obj.battle;
          }
        }
      });
    });
    socket.on("start-battle", function(data) {
      battle = new Battle({
        'squareHeight': 60,
        'gameHolder': $('#map')
      });
      ready = 0;
      battle.init();
      battleId = data.battleId;
      $.get('/battle/get-details/', {
        'battleId': battleId
      }, function(data) {
        var obj, user1, user2;
        obj = $.parseJSON(data);
        user1 = obj.user1;
        user2 = obj.user2;
        $('#lvl1').html("level: " + user1.lvl);
        $('#lvl2').html("level: " + user2.lvl);
        $('#won1').html("won: " + user1.won);
        $('#won2').html("won: " + user2.won);
        $('#lost1').html("lost: " + user1.lost);
        $('#lost2').html("lost: " + user2.lost);
        $('#img1').attr('src', "/static/img/user/lobby/avioane/" + user1.avion + ".png");
        $('#img2').attr('src', "/static/img/user/lobby/avioane/" + user2.avion + ".png");
        $('#versus_p1_name').html(user1.username);
        $('#versus_p2_name').html(user2.username);
        $('#sub_holder').remove();
        $('#lobby').remove();
        $('#sub_header_holder').remove();
        $('#versus').css('display', 'block');
        return setTimeout(function() {
          return $('#versus').fadeOut('slow', function() {
            $("#battle").fadeIn(500).css('display', 'block');
            $("#start_battle_button").fadeIn(500).css('display', 'block');
            timer = new Countdown("#time_left", "60", function() {
              return $.post('/battle/', {
                'state': 'loss',
                'enemy': enemy,
                'battleId': battleId
              }, function(data) {
                socket.emit("finish", {
                  battleId: battleId,
                  user: id
                });
                $('#notificationBig').attr('class', 'alert notification');
                $('#notificationBig').html("You lost").dequeue().stop().slideDown(200).delay(1700).slideUp(200, function() {
                  return window.location = '/';
                });
                return myTurn = false;
              });
            });
            return timer.init();
          });
        }, 3000);
      });
      if (data.firstUser === id) {
        return enemy = data.secondUser;
      } else {
        return enemy = data.firstUser;
      }
    });
    socket.on("ready", function(data) {
      if (username !== data) {
        ready += 1;
        if (war.ready !== void 0) {
          war.ready = ready;
        }
        if (ready === 2) {
          $('#notificationSmall').attr('class', 'succes notification');
          $('#notificationSmall').html("Start battle!").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
          war.move_timer = new Countdown("#time_left", "10", function() {
            return war.sendData("next-turn", {
              enemy: enemy
            });
          }, $('#notificationSmall').attr('class', 'alert notification'), $('#notificationSmall').html("To late!").dequeue().stop().slideDown(200).delay(1700).slideUp(200), myTurn = false);
          return war.move_timer.init();
        } else {
          $('#notificationSmall').attr('class', 'info notification');
          return $('#notificationSmall').html("Your enemy is ready to play!").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
        }
      }
    });
    socket.on("check-hit", function(data) {
      var x, y;
      war.myTurn = true;
      $('#notificationSmall').attr('class', 'succes notification');
      $('#notificationSmall').html("It's your turn!").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
      war.move_timer = new Countdown("#time_left", "10", function() {
        war.sendData("next-turn", {
          enemy: enemy
        });
        $('#notificationSmall').attr('class', 'alert notification');
        $('#notificationSmall').html("To late!").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
        return myTurn = false;
      });
      war.move_timer.init();
      x = data.coordinates.x;
      y = data.coordinates.y;
      return $.post('/battle/attack/', {
        'x': x,
        'y': y,
        'battleID': battleId
      }, function(data) {
        if (data === 'miss') {
          return war.miss_attack(x, y, 0, 60 * 11 - 25);
        } else {
          if (data === 'hit') {
            return war.hit_attack(x, y, 0, 60 * 11 - 25);
          } else {
            if (data === 'finished') {
              return $.post('/battle/', {
                'state': 'loss',
                'enemy': enemy,
                'battleId': battleId
              }, function(data) {
                socket.emit("finish", {
                  battleId: battleId,
                  user: id
                });
                $('#notificationBig').attr('class', 'alert notification');
                $('#notificationBig').html("You lost").dequeue().stop().slideDown(200).delay(1700).slideUp(200, function() {
                  return window.location = '/';
                });
                return myTurn = false;
              });
            } else {
              return war.head_attack(x, y, 0, 60 * 11 - 25);
            }
          }
        }
      });
    });
    socket.on("win", function() {
      $('#notificationSmall').attr('class', 'succes notification');
      $('#notificationSmall').html("You won").dequeue().stop().slideDown(200).delay(1700).slideUp(200, function() {
        return window.location = '/';
      });
      return myTurn = false;
    });
    socket.on("miss", function(data) {
      var x, y;
      x = data.coordinates.x;
      y = data.coordinates.y;
      war.draw_attack({
        x: x * war.map.squareHeight + war.map.position.left,
        y: y * war.map.squareHeight + war.map.position.top,
        height: war.map.squareHeight,
        fillStyle: "#FFF"
      });
      $('#notificationSmall').attr('class', 'alert notification');
      return $('#notificationSmall').html("Miss!").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
    });
    socket.on("hit", function(data) {
      var x, y;
      x = data.coordinates.x;
      y = data.coordinates.y;
      war.draw_attack({
        x: x * war.map.squareHeight + war.map.position.left,
        y: y * war.map.squareHeight + war.map.position.top,
        height: war.map.squareHeight,
        fillStyle: "blue"
      });
      $('#notificationSmall').attr('class', 'info notification');
      return $('#notificationSmall').html("Hit!").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
    });
    socket.on("head", function(data) {
      var x, y;
      x = data.coordinates.x;
      y = data.coordinates.y;
      war.draw_attack({
        x: x * war.map.squareHeight + war.map.position.left,
        y: y * war.map.squareHeight + war.map.position.top,
        height: war.map.squareHeight,
        fillStyle: "yellow"
      });
      $('#notificationSmall').attr('class', 'succes notification');
      return $('#notificationSmall').html("OMG a head!").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
    });
    socket.on("next-turn", function(data) {
      myTurn = true;
      return $('#notificationSmall').html("It's your turn!").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
    });
    socket.on("disconnectGame", function(data) {
      $.post('/battle/disconnect/', {
        'enemy': enemy,
        'battleID': battleId,
        "state": "loss"
      }, function() {
        $('#notificationBig').attr('class', 'succes');
        return $('#notificationBig').html("You won").dequeue().stop().slideDown(200).delay(1700).slideUp(200, function() {
          return window.location = '/';
        });
      });
      return myTurn = false;
    });
    socket.on("receive-invitation", function(data) {
      var html;
      $('#notificationBig').attr('class', 'alert notification');
      html = "<div id='invitation-notification' data-id='" + data.id + "' >" + data.username + " wants to battle you! Do you accept the battle? <a id='accept-invitation' class='button'>Yes</a> or <a class='button'>No</a></div>";
      return $('#notificationBig').html(html).dequeue().stop().slideDown(200);
    });
    $("#accept-invitation").live("click", function() {
      var id;
      id = $(this).parent().data('id');
      $.get('battle/accept-invitation/', {
        userid: id
      }, function(data) {});
      $(this).parent().parent().slideUp(200);
      return myTurn = true;
    });
    $("#start_battle_button").click(function() {
      var checked;
      checked = battle.checkReady(battleId);
      if (checked) {
        $("#start_battle_button").remove();
        timer.clearMyInterval();
        ready += 1;
        war = new War({
          'user': id,
          'enemy': enemy,
          'battleId': battleId,
          'userSocket': socket,
          'map': checked,
          'myTurn': myTurn,
          'ready': ready,
          'move_timer': move_timer
        });
        return war.map.canvas.onmousedown = function(e) {
          return war.checkMouseDown(e);
        };
      }
    });
    return $("li:[data-id]").live("click", function(e) {
      var id;
      id = $(this).data("id");
      $.post("/battle/send-invitation/", {
        toUserId: id
      }, function(data) {
        if (data === 'not-ready') {
          $('#notificationBig').attr('class', 'alert notification');
          return $('#notificationBig').html("You can't invite him right now! He is already invited!").dequeue().stop().slideDown(200).delay(2000).slideUp(200);
        } else {
          if (data === 'battle') {
            $('#notificationBig').attr('class', 'alert notification');
            return $('#notificationBig').html("Your buddy is in a battle! Wait for him to finish!").dequeue().stop().slideDown(200).delay(2000).slideUp(200);
          } else {
            $('#notificationBig').attr('class', 'info notification');
            return $('#notificationBig').html("Ready for battle!").dequeue().stop().slideDown(200).delay(1700).slideUp(200);
          }
        }
      });
      return myTurn = false;
    });
  });

}).call(this);
