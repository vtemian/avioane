class Map
  constructor: (@options) ->
    @m_canvas = document.createElement('canvas')
    @m_canvas.width = @options.width
    @m_canvas.height = @options.height

    $('#initial-game').append @m_canvas

    @draw_map()

  draw_map: ->
    context = @m_canvas.getContext("2d")
    imageObj = new Image()

    imageObj.onload = ->
        context.drawImage(imageObj, 69, 50)

    imageObj.src = "http://www.html5canvastutorials.com/demos/assets/darth-vader.jpg"


class Game
  constructor: (@firstOponent, @secondOponent) ->
    @map = new Map({
      'width': 1000
      'height': 3000
    })

$(document).ready ->
  game = new Game('george', 'asd')
  console.log game
