$(document).ready ->
  $.get('/shop/items/',
    (data) ->
      obj = $.parseJSON(data)
      what_i_can_buy = obj.what_i_can_buy
      what_i_cant_buy = obj.what_i_cant_buy


      $.each(what_i_can_buy, (index, item) ->
        item =  $.parseJSON(item)
        name = Object.keys(item)[0]
        image = "/static/img/store/weapons/"+item[name].image+".png"
        html = "<li class='clearfix'>\
            <div class='weapon_left'>\
            <div class='weapon_name'>"+name+"</div>\
            <div class='weapon_image'><img src='"+image.toString()+"' alt='shield'/></div>\
            </div>\
            <div class='weapon_middle'>\
            <span class='weapon_cost'>Cost: "+item[name].cost+"$</span>\
            <p class='weapon_description'>"+item[name].description+"</p>\
            </div>\
            <div class='weapon_right'>\
            <span class='weapon_pcs'>pieces:</span><input class='weapon_pcs_input' type='number' required />\
            <div class='weapon_buy buy_button' data-description='"+item[name].description+"' data-item='" + name + "' data-image='"+item[name].image+"' data-costs='" + item[name].cost + "'>buy</div>\
            </div>\

            </li>\
        "

        $('#unlocked_weapons').prepend(html)

      )

      $.each(what_i_cant_buy, (index, item) ->
          item =  $.parseJSON(item)
          name = Object.keys(item)[0]
          image = "/static/img/store/weapons/"+item[name].image+".png"
          html = "<li class='clearfix'>
            <div class='weapon_left'>
            <div class='weapon_name'>"+name+"</div>
            <div class='weapon_image'><img src='"+image.toString()+"' alt='shield'/></div>
            </div>
            <div class='weapon_middle'>
            <span class='weapon_cost'>Cost: "+item[name].cost+"$</span>
            <p class='weapon_description'>"+item[name].description+"</p>
            </div>
            <div class='weapon_right'>
            </div>

            </li>
          "
          $('#all_weapons').prepend(html)
      )
  )
  $('.buy_button').live('click',
    ->
      item = $(this).data('item')


      image = $(this).data('image')
      description = $(this).data('description')
      volum = $(this).prev().val()
      cost = $(this).data('costs')

      if volum * cost > money
        $('#notificationBig').attr('class', 'alert notification')
        $('#notificationBig').html("You don't have enough money!").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
      else

        $.post('/shop/buy/', {'item':item, 'volum':volum, 'cost': cost, 'image':image, 'description': description},
          (data) ->
            $('#notificationBig').attr('class', 'succes notification')
            $('#notificationBig').html("Got it!"+" -"+volum*cost+"$").dequeue().stop().slideDown(200).delay(1700).slideUp(200)
        )
        $(this).prev().val(0)

  )
