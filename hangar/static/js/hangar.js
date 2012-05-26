/* Author: arghy

 */

$(function(){

    /* =============================================================================
     Hangar Page
     ========================================================================== */

    /* Dragabble Weapons */
    $('#weapon_info>ul>li').fadeIn(700);
    $('.weapon').draggable({containment:'#hangar',revert:true,scroll:false});
    $( "#plane_holder" ).droppable({
        drop: function( event, ui ) {
            $explodatu = $(ui.draggable);
            $(ui.draggable).hide("explode",1000);


            var weapon_type = $(ui.draggable).data('type');
            var image = $(ui.draggable).data('image');

            $.post('/hangar/equip/', {'name': weapon_type}, function(data){
                if(data == 'ok'){
                    my_html = "<li data-info='"+weapon_type+"'><img src='/static/img/store/weapons/"+image+".png'  alt='"+weapon_type+"' /><ul class='weapon_stats'><li>"+weapon_type+": Level 1</li><li>Scan range: 8%</li></ul><div class='weapon_change'>remove</div></li>"
                    $('#used_weapons').append(my_html);
                }
                else{
                    $explodatu.fadeIn(500);

                }
            });

        }
    });

    $('.weapon_change').live("click", function (){
        var name = $(this).parent().data('info')
        $li = $(this).parent();
        $.post('/hangar/dequip/', {'name': name}, function(data){
            $li.fadeOut(400,$li.remove())
        });
    })
    $('#buy_weapons').click(function(){
        window.location = '/shop'
    })
});

