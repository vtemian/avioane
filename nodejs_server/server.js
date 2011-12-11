var io = require('socket.io').listen(5551);
var users = new Array();
var clients = new Array();
var game = new Array();

io.sockets.on('connection', function (socket) {
    socket.emit('identified', { message: 'handshaking' });

    socket.on('handshaking', function (data) {
        users.push(data.user);
        clients.push(socket);
        for(var i=0; i<clients.length; i++){
            clients[i].emit('on', {'online': clients.length});
        }
    });

    socket.on('game', function(data){
       var user = users.indexOf(data.user);
       if(game.length>0 && (game.indexOf(clients[user]) == -1)){
          game[0].emit('battle', {'enemy': data.user, 'free': true})
          var user1 = clients.indexOf(game[0]);
          socket.emit('battle', {'enemy': users[user1], 'free': false});
          game.splice(0, 1);
       }else{
           if(!game.length)
                game.push(clients[user]);
       }
    });
    socket.on('loss', function(data){
        console.log('a');
       var user = users.indexOf(data.enemy);
       var enemy = clients.indexOf(socket);
       clients[user].emit('loss', {'enemy': users[enemy]});
    });
    socket.on('ready', function(data){
       var user = users.indexOf(data.enemy);
       var enemy = clients.indexOf(socket);
       clients[user].emit('ready', {'enemy': users[enemy]});
    });
    socket.on('attack', function(data){
       var user = users.indexOf(data.enemy);
       if(user != -1){
           var enemy = clients.indexOf(socket);
           clients[user].emit('attack', {'x': data.x, 'y': data.y});
       }
    });
    socket.on('hit', function(data){
       var user = users.indexOf(data.enemy);
       if(user != -1){
           var enemy = clients.indexOf(socket);
            if(data.plane == undefined)
                clients[user].emit('hit', {'x': data.x, 'y': data.y});
            else
                clients[user].emit('hit', {'x': data.x, 'y': data.y, 'plane': data.plane});
        }
    });
    socket.on('missed', function(data){
       var user = users.indexOf(data.enemy);
       if(user != -1){
           var enemy = clients.indexOf(socket);
           clients[user].emit('missed', {'x': data.x, 'y': data.y});
       }
    });
    socket.on('disconnect', function (data){
        var index = clients.indexOf(socket)
        clients.splice(index, 1)
        users.splice(index, 1)
        var index = game.indexOf(socket);
        if(index != -1){
            game.splice(index, 1);
        }
        for(var i=0; i<clients.length; i++){
            clients[i].emit('on', {'online': clients.length});
        }
    });

});