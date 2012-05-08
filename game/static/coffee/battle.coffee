#set up the battle
class Battle

    constructor: (opts) ->
        @squareHeight = opts.squareHeight
        @gameHolder = opts.gameHolder

        @canvasWidth = @squareHeight * 10 * 2 + @squareHeight * 2
        @canvasHeight = @squareHeight * 10 + 5 * @squareHeight

        @map = null
        @collissions = null
        @frontend = null

#    Generating the map canvas and pass the canvas context to Map object
    createMap:(top, left, width, height) ->
        mapCanvas = document.createElement('canvas')
        mapCanvas.width = width
        mapCanvas.height = height

        @gameHolder.append(mapCanvas)

        context = mapCanvas.getContext('2d')
        @map = new Map({
            'context': context,
            'position': {'top': top, 'left': left},
            'squareHeight': @squareHeight
        })

        return mapCanvas

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
                'position': {'top': @squareHeight * 11, 'left': (@squareHeight * 5 * order)},
                'squareHeight': @squareHeight,
                'droppingArea': @map,
                'order': order
            })
            @frontend.addPlane(plane)

    checkReady: ->
      console.log @checkPlanes()
      if @checkPlanes()
        return @createMap(0, @canvasWidth, 2 * @canvasWidth, @canvasHeight)
      else
        return false

    checkPlanes: ->
      for plane in @frontend.planes
        if plane.isNotReady
          return false
      return true

    init: ->
        @createMap(0, 0, @canvasWidth, @canvasHeight)

        @frontend = new Frontend(@map)

        @createPlanes(3)
        @createCollissions(@frontend)

    

window.Battle = Battle