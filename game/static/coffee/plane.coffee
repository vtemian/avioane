#A plane object
class Plane
    constructor: (opts) ->
        @context = opts.context
        @position = opts.position
        @squareHeight = opts.squareHeight
        @startPosition = @position
        @droppingArea = opts.droppingArea
        @order = opts.order
        @avion = opts.avion
        @matrixPosition = []

        @draggable = false
        @droppeable = true
        @deltaClickPosition = []

        @isNotReady = true

        @format = [
          [
              {'y': 0, 'x':2},
              {'y': 1, 'x':0},
              {'y': 1, 'x':1},
              {'y': 1, 'x':2},
              {'y': 1, 'x':3},
              {'y': 1, 'x':4},
              {'y': 2, 'x':2},
              {'y': 3, 'x':1},
              {'y': 3, 'x':2},
              {'y': 3, 'x':3},
          ],
          [
            {'y': 2, 'x':0},
            {'y': 0, 'x':1},
            {'y': 1, 'x':1},
            {'y': 2, 'x':1},
            {'y': 3, 'x':1},
            {'y': 4, 'x':1},
            {'y': 2, 'x':2},
            {'y': 1, 'x':3},
            {'y': 2, 'x':3},
            {'y': 3, 'x':3},
          ],
          [
            {'y': 3, 'x':2},
            {'y': 2, 'x':0},
            {'y': 2, 'x':1},
            {'y': 2, 'x':2},
            {'y': 2, 'x':3},
            {'y': 2, 'x':4},
            {'y': 1, 'x':2},
            {'y': 0, 'x':1},
            {'y': 0, 'x':2},
            {'y': 0, 'x':3},
          ],
          [
            {'y': 2, 'x':3},
            {'y': 0, 'x':2},
            {'y': 1, 'x':2},
            {'y': 2, 'x':2},
            {'y': 3, 'x':2},
            {'y': 4, 'x':2},
            {'y': 2, 'x':1},
            {'y': 1, 'x':0},
            {'y': 2, 'x':0},
            {'y': 3, 'x':0},
          ]
        ]
#        @draw()
        @orientation = 0
        @fillStyle = "#71b44b"
        @collesionFillStyle = '#FFF'
        #create each plane have it's own canvas to optimize the drawing time
        @m_canvas = document.createElement('canvas')
        @m_canvas.width = 1000
        @m_canvas.height = 500

        @drawRenderedPlane()


    #generate the plane
    drawRenderedPlane: ->

        m_context = @m_canvas.getContext('2d')
        m_context.fillStyle = @fillStyle
        m_context.clearRect 0, 0, @squareHeight * 5, @squareHeight * 5

        for component in @format[@orientation]
                  x = component.x * @squareHeight
                  y = component.y * @squareHeight
                  m_context.fillRect x, y, @squareHeight, @squareHeight

        @draw()

    #with our plane canvas, we don't need to delete the hole canvas, just redraw it
    draw: ->
#      context = @context
#      position = @position
#      img = new Image();
#      img.onload = ->
#        context.drawImage(img, position.top, position.left, 150, 150)
#      img.src =  "/static/img/user/lobby/avioane/" + @avion + ".png"

        @context.drawImage(@m_canvas, @position.top, @position.left)

    #setting up the position
    setPosition: (newPosition) ->
        #clear the old plane
        @clearRect()
        #set new position
        @position = newPosition
        console.log "asd"
        #redraw it
        @draw()

    #delete the plane
    clearRect: ->
        @context.clearRect @position.top, @position.left, @squareHeight * 5, @squareHeight * 5

    #rotate the plane
    rotatePlane: ->
      @orientation = (@orientation + 1) % 4

      @clearRect()
      @drawRenderedPlane()
      @dropPlane()

      true

    #check if the click it's on the plane, no near it
    checkMouseDown: (e) ->
        x = e.layerX
        y = e.layerY

        for component in @format[@orientation]
            componentX = component.x * @squareHeight + @position.top

            componentY = component.y * @squareHeight + @position.left
            if x >= componentX and y >= componentY and x <= componentX + @squareHeight and y <=componentY + @squareHeight
                if e.which == 3

                  @rotatePlane()
                else
                  @deltaClickPosition =
                      x: x - @position.top
                      y: y - @position.left
                  @draggable = true
                  return true

        @draggable = false
        return false

    #change and redraw the position
    movePlane: (e) ->
        if @draggable
            x = e.layerX
            y = e.layerY

            newPosition =
                top: x - @deltaClickPosition.x
                left: y - @deltaClickPosition.y

            if @checkDropPosition newPosition
                @adjustPosition newPosition
                return true
            else
                @setPosition newPosition
                return false

    #get the position in an array(old style position method)
    setMatrixPosition: ->
        @matrixPosition = []
#       line:0 column:0 in pixels of the plane
        x = @position.top / @squareHeight
        y = @position.left / @squareHeight

        check = false

        for component in @format[@orientation]
            #check if the plane is not on the map
            if x + component.x < 0 or x + component.x > 9 or y + component.y < 0 or y + component.y > 9
              check = true

            @matrixPosition.push
                x: x + component.x
                y: y + component.y

        console.log @matrixPosition

        @isNotReady = check

    #if the plane is in the map, adjust the position to fit on the squares
    adjustPosition: (newPosition) ->
        if newPosition.top % @squareHeight > @squareHeight / 2
            newPosition.top = parseInt(newPosition.top / @squareHeight) * @squareHeight + @squareHeight
        else
            newPosition.top = parseInt(newPosition.top / @squareHeight) * @squareHeight

        if newPosition.left % @squareHeight > @squareHeight / 2
            newPosition.left = parseInt(newPosition.left / @squareHeight) * @squareHeight+ @squareHeight
        else
            newPosition.left = parseInt(newPosition.left / @squareHeight) * @squareHeight

        @setPosition(newPosition)
        @setMatrixPosition()


    #checking if the plane it's on the map area
    checkDropPosition: (newPosition) ->
        x = newPosition.top
        y = newPosition.left

        minX = @droppingArea.position.top - @squareHeight / 2
        minY = @droppingArea.position.left - @squareHeight / 2

        if @orientation % 2 == 0
          maxX = @droppingArea.width - @squareHeight * 5 + @squareHeight / 2
          maxY = @droppingArea.height - @squareHeight * 4 + @squareHeight / 2
        else
          maxX = @droppingArea.width - @squareHeight * 4 + @squareHeight / 2
          maxY = @droppingArea.height - @squareHeight * 5 + @squareHeight / 2

#        check if plane is on the map

        if x > minX and x < maxX and y > minY and y < maxY
            return true
        else
            return false
    #if the plane can be dropped, than drop it
    dropPlane: (e) ->
        if @droppeable
            @draggable = false
            if @checkDropPosition @position

                @adjustPosition @position
            else
                @setMatrixPosition()
                @setPosition(@startPosition)


window.Plane = Plane