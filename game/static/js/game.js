$(document).ready(function(){
    var enemy = '';
    var planes = {
            plane1: new Array(),
            plane2: new Array(),
            plane3: new Array()
    };
    var battle = '';
    var meReady = enemyReady = attackReady = false;
    var free;
    var win = 0;
    var planePositions = {
        1: new Array("00100", "11111", "00100", "01110"),
        2: new Array("00100", "11111", "00100", "01110"),
        3: new Array("00100", "11111", "00100", "01110"),
        4: new Array("00100", "11111", "00100", "01110")
    };
    gen_plane($('#plane1'), planePositions['1']);
    $('#plane1').hover(function(){
        console.log('hoverIN!');
    }, function(){
        console.log('hoverOUT!');
    });
    $('#container1').css('display', 'n33333333333333333333333333333sx44ddddddddddddddddddddddddddddddddd' +
        'ddddddddqone');
    $('#container2').css('display', 'none');
    $('#join-battle').live('click' ,function(){
        socket.emit('game', {'user': username});
        $('#stats').append('<div id="loading">Just w8!</div>');
        $(this).remove();
    });
    socket.on('on', function(data){
        $('#online').html(data.online);
    });
    socket.on('battle', function (data) {
        enemy = data.enemy;
        free = data.free;
        $('#rank').remove();
        gen_map($('#map1'), '');
        $('#container1').css('display', 'block');
        //gen_plane($('#plane1'));
        gen_plane($('#plane2'), new Array("00100", "11111", "00100", "01110"));
        gen_plane($('#plane3'), new Array("00100", "11111", "00100", "01110"));
        //we are ready for battle!
        //Create a battle in backend!
        $.post('/battle/create/', {'enemy': enemy}, function(battleID){
                battle = battleID;                  //get battle's id
        });
        socket.emit('createBattle', {'user': username, 'enemy': enemy, 'battleID': battle});
        $(".plane").draggable({
            revert: "invalid",
            grid: [42, 42] ,
            snap: '.hitPoint',
            containment: [$("#map1").offset().left, $("#map1").offset().top, $("#map1").offset().left + 210, $("#map1").offset().top + 292],
            stop: function(event, ui) {
                var left = ui.offset.left;
                var top = ui.offset.top;
                var i = parseInt((top-$("#map1").offset().top)/42);
                var j = parseInt((left-$("#map1").offset().left)/42);

                planes[$(this).attr('id')] = get_position(i, j, 1);

                $('.collision').removeClass('collision');

                var coll1 = check_collesion(planes['plane1'], planes['plane2']);
                var coll2 = check_collesion(planes['plane1'], planes['plane3']);
                var coll3 = check_collesion(planes['plane2'], planes['plane3']);

                return true;
            }
        });
        $('#map1').droppable({ accept: '.plane' , tolerance: 'fit' });
        $('#loading').html('<span id="wait">Ready!</span>');
    });
    $('#wait').live('click', function(){
        if(planes['plane1'].length && planes['plane2'].length && planes['plane3'].length){
            if(check_collesion(planes['plane1'], planes['plane2']) || check_collesion(planes['plane1'], planes['plane3']) || check_collesion(planes['plane2'], planes['plane3'])){
                alert('There are some collesion on the map...take care!');
            }else{
                lock_planes();
                meReady = true;
                if(!$('#enemy').length)
                    $('#stats').append('<div id="ready">Wait for opponent....</div>');
                socket.emit('ready', {'enemy': enemy});

                $(this).remove();
                if(enemyReady){
                    attackReady = true;
                    if(free){
                        $('#turn').html("It's your turn!");
                    }else{
                        $('#turn').html("It's "+enemy+" turn!");
                    }
                }
                //send planes positions to backend
                send_plane(planes['plane1'], 'plane1');
                send_plane(planes['plane2'], 'plane2');
                send_plane(planes['plane3'], 'plane3');
            }
        }else{
            alert('You must place the planes!');
        }
    });
    //TODO: see if planes were creted!
    function send_plane(plane, type){
        $.each(plane, function(index, value){
            $.post('/plane/create_positioning/'+type+'/', {'battleID': battle, 'x': value.top, 'y': value.left}, function(data){
                console.log(data);
            });
        });
    }
    socket.on('ready', function(data){
        enemyReady = true;
        $('#stats').append('<div id="enemy">'+data.enemy+' is ready!</div>');
        $('#ready').remove();
        gen_map($('#map2'), 'attack');
        $('#container2').css('display', 'block');
        if(meReady){
            attackReady = true;
            if(free){
                $('#turn').html("It's your turn!");
            }else{
                $('#turn').html("It's "+enemy+" turn!");
            }
        }
    });
    socket.on('attack', function(data){
        var x = data.x;
        var y = data.y;
        //attack sent to backend
        $.post('/battle/attack/', {'x': x, 'y':y, 'battleID':battle}, function(data){
            console.log(data)
            if(data == 'miss'){
                miss_attack(x, y);
            }else{
                if(data == 'hit'){
                    hit_attack(x, y);
                }else{
                    if(data == 'finished'){
                        $('#win-loss').html('YOU LOST!');
                        socket.emit('loss', {'enemy': enemy});
                        $.post('/battle/', {'state': 'loss', 'enemy': enemy}, function(data){
                            finish_battle();
                        });
                    }else{
                        head_attack(data, x, y);
                    }
                }
            }
        });
        free = true;
        $('#turn').html("It's your turn!");

    });
    //miss
    function miss_attack(x, y){
        $("#cell-" + x + "-" + y + "-").addClass('missedMe');
        socket.emit('missed', {'x': x, 'y': y, 'enemy': enemy});
    }
    //normal hit(not head)
    function hit_attack(x, y){
        $("#cell-" + x + "-" + y + "-").addClass('hitMe');
        socket.emit('hit', {'x': x, 'y': y, 'enemy': enemy});
    }
    //head attack
    function head_attack(data, x, y){
        $.each(planes[data], function(index, value){
                $('#cell-' + value.top + '-' + value.left + '-').addClass('hitHead');
        });
        socket.emit('hit', {'x': x, 'y': y, 'enemy': enemy, 'plane': planes[data]});
    }
    //finish the battle
    function finish_battle(){
        $('#content').remove();
        $('#win-loss').modal({
            onOpen: function (dialog) {
                var sm = this;

                dialog.overlay.slideDown('slow', function () {
                    dialog.data.hide();
                    dialog.container.slideDown('slow', function () {
                        dialog.data.slideDown('slow');
                    });
                });
                dialog.container.animate({height: 100, width: 300}, 500, function () {
                    sm.setPosition();
                });
            },
            onClose: function (dialog) {
                dialog.data.slideUp('slow', function () {
                    dialog.container.hide('slow', function () {
                        dialog.overlay.slideUp('slow', function () {
                            $.modal.close();
                        });
                    });
                });
                window.location = '/';
            }
        });
    }
    socket.on('loss', function(data){
        finish_battle();
    });
    socket.on('disconnectGame', function(data){
        $.post('/battle/disconnect/', {'enemy': enemy, 'battleID': battle}, function(data){
            finish_battle();
        });
    });
    socket.on('hit', function(data){
        var x = data.x;
        var y = data.y;
        if(data.plane == undefined)
            $('#cell-' + x + '-' + y + '-attack').addClass('hitAttack');
        else{
            //draw dead plane
            $('#cell-' + x + '-' + y + '-attack').addClass('hitHead');
            $('#cell-' + x + '-' + y + '-attack').removeClass('attack');
            $.each(data.plane, function(index, value){
                $('#cell-' + value.top + '-' + value.left + '-attack').removeClass('attack');
                $('#cell-' + value.top + '-' + value.left + '-attack').addClass('hitHead');
            });
        }
    });
    socket.on('missed', function(data){
        var x = data.x;
        var y = data.y;
        $('#cell-' + x + '-' + y + '-attack').addClass('missedAttack');
    });
    $('.attack').live('click', function(){
        if(free && attackReady){
            var x = $(this).data('x');
            var y = $(this).data('y');
            socket.emit('attack', {'x': x, 'y': y, 'enemy': enemy});
            free = false;
            $('#turn').html("It's "+enemy+" turn!");
            $(this).removeClass('attack');
        }else if(!free){
            alert("It's not your turn!");
        }else{
            alert("You can't attack right now...everybody have to be ready!");
        }
    })
});
function random_place(){
    
}
function lock_planes(){
    $('#plane1').draggable({ disabled: true });
    $('#plane2').draggable({ disabled: true });
    $('#plane3').draggable({ disabled: true });
}
function gen_plane($container, plane){

    for(var i=0; i<=3; i++){
        var $line = '<div id="row-'+i+'" class="line">';
        var spans = '';
        for(var j=0; j<=4; j++){
            var classplane = 'hitPoint-plane';
            if(plane[i][j] == '1'){
                classplane = 'planeComp';
            }
             spans += '<span data-x="'+i+'" data-y="'+j+'" class="' + classplane + '"></span>';
        }
        $line += spans;
        $line += '</div>';
        $container.append($line);
    }

}
function gen_map($container, classSqr){
    for(var i=0; i<10; i++){
        var $line = '<div id="row-'+i+'" class="line">';
        var spans = '';
        for(var j=0; j<10; j++){
            spans += '<span id="cell-' + i + '-' + j + '-' + classSqr + '" data-x="'+i+'" data-y="'+j+'" class="hitPoint '+ classSqr +'"></span>';
        }
        $line += spans;
        $line += '</div>';
        $container.append($line);
    }
}
function get_position(top, left, position){
    var planeComps = new Array();
    if(position == 1){
        planeComps[0] = {'left': left+2, 'top':top};
        planeComps[1] = {'left': left, 'top':top+1};
        planeComps[2] = {'left': left+1, 'top':top+1};
        planeComps[3] = {'left': left+2, 'top':top+1};
        planeComps[4] = {'left': left+3, 'top':top+1};
        planeComps[5] = {'left': left+4, 'top':top+1};
        planeComps[6] = {'left': left+2, 'top':top+2};
        planeComps[7] = {'left': left+1, 'top':top+3};
        planeComps[8] = {'left': left+2, 'top':top+3};
        planeComps[9] = {'left': left+3, 'top':top+3};
    }
    return planeComps;
}
function check_collesion(plane1, plane2){
    var collesion = false;
    if(plane1.length == 0 || plane2.length == 0) { return false; }
    
    for(var i=0; i<10; i++){
        for(var j=0; j<10; j++){
            if((plane1[i].left == plane2[j].left)&&(plane1[i].top == plane2[j].top)){
                $("#cell-" + plane1[i].top + "-" + plane1[i].left + "-").addClass('collision');
                $("#cell-" + plane2[j].top + "-" + plane2[j].left + "-").addClass('collision');
                collesion = true;
            }
        }
    }
    
    return collesion;
}