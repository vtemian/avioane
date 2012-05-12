#manage the movement on the canvas
class Frontend
    constructor: (@map) ->
        @planes = []
        @collession = false
        @collessions = null

    addPlane: (plane) ->
        @planes.push(plane)

    checkMouseDown: (e) ->

        for plane in @planes
            if plane.checkMouseDown e
                return true
        return false

    checkMouseMove: (e) ->
        for plane in @planes
            if plane.draggable
                plane.movePlane e
                @collissions.resetCollissions()

                @collession = (@collissions.checkCollissions(@planes[0], @planes[1]) == @collissions.checkCollissions(@planes[0], @planes[2]))
                @collession = (@collession == @collissions.checkCollissions(@planes[1], @planes[2]))

                @collissions.drawCollissions()

                plane.droppeable = !@collession



    checkMouseUp: (e) ->
      for plane in @planes
          if plane.draggable
              plane.dropPlane e

window.Frontend = Frontend