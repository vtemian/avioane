#set up the battle
class Battle

    constructor: (opts) ->
        @squareHeight = opts.squareHeight
        @gameHolder = opts.gameHolder

        @avion = opts.avion

        @canvasWidth = @squareHeight * 10 * 2 - 200
        @canvasHeight = @squareHeight * 10

        @map = null
        @collissions = null
        @frontend = null

#    Generating the map canvas and pass the canvas context to Map object
    createMap:(top, left, width, height, squareHeight) ->
        mapCanvas = document.createElement('canvas')
        mapCanvas.width = width
        mapCanvas.height = height

        @gameHolder.append(mapCanvas)

        context = mapCanvas.getContext('2d')
        @map = new Map({
            'context': context,
            'position': {'top': top, 'left': left},
            'squareHeight': squareHeight,
            'canvas': mapCanvas
        })

        return @map

#     1.generating the collissions canvas and pass the context
#       and the Map object to the Collissions obj
#     2. it's the final layer, so it get also all the mouse events

    createCollissions:(frontend) ->
        collissionsCanvas = document.createElement('canvas')
        collissionsCanvas.width = @canvasWidth
        collissionsCanvas.height = @canvasHeight

        @gameHolder.append(collissionsCanvas)

        context = collissionsCanvas.getContext('2d')
        @collissions = new Collissions({
            'holder': @map,
            'context': context
            'canvas': collissionsCanvas
        })

        frontend.collissions  = @collissions

        collissionsCanvas.onmousedown = (e) ->
            frontend.checkMouseDown e
        collissionsCanvas.onmousemove = (e) ->
            frontend.checkMouseMove e
        collissionsCanvas.onmouseup = (e) ->
            frontend.checkMouseUp e

#       Create the planes and put them into frontend object

    createPlanes: (maxPlaneNumber) ->
        for order in [0..maxPlaneNumber-1]
            planeCanvas = document.createElement('canvas')
            planeCanvas.width = @canvasWidth
            planeCanvas.height = @canvasHeight

            @gameHolder.append(planeCanvas)

            context = planeCanvas.getContext('2d')
            plane = new Plane({
                'context': context,
                'position': {'top': @squareHeight * 11 - 40, 'left': 10},
                'squareHeight': @squareHeight,
                'droppingArea': @map,
                'order': order,
                'avion': @avion
            })
            @frontend.addPlane(plane)

    checkReady: (battleId)->
      if @checkPlanes()
        console.log "asddddddddd"
        $('canvas').remove()
        map = @createMap(0, @squareHeight*11 - 25,  @canvasWidth, @canvasHeight, 27)
        context = map.canvas.getContext('2d')
        $('#mini_map').addClass('textura')
        map = @createMap(0, 0, @canvasWidth, @canvasHeight, @squareHeight)
        for plane, index in @frontend.planes
          context.fillStyle = plane.fillStyle
          type = "plane" + (index+1)
          for coordinate, myIndex in plane.matrixPosition
              $.post('/plane/create_positioning/'+type+'/', {'battleID': battleId, 'x': coordinate.x, 'y': coordinate.y, 'head': myIndex}, (data)->
                console.log type
              )
              context.beginPath()
              context.rect coordinate.x*27+@squareHeight*11 - 25, coordinate.y*27, 27, 27
              context.fill()

        return map
      else
        return false

    checkPlanes: ->
      for plane in @frontend.planes
        plane.setMatrixPosition()
        if plane.isNotReady
          return false
      return true

    init: ->
        @createMap(0, 0, @canvasWidth, @canvasHeight, @squareHeight)

        @frontend = new Frontend(@map)

        @createPlanes(3)
        @createCollissions(@frontend)

    

window.Battle = Battle