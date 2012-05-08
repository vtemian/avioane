#manage the collissions on the battle map
class Collissions
    constructor: (opts) ->
        @squareHeight = opts.holder.squareHeight
        @position = opts.holder.position
        @context = opts.context
        @canvas = opts.canvas

        @collissions = []
        @fillStyle = "#FFF"
        #disable right click
        @canvas.oncontextmenu = ->
          return false
    resetCollissions: ->
        @collissions = []
        @clearRect()

    clearRect: ->
            @context.clearRect @position.top, @position.left, @squareHeight * @squareHeight, @squareHeight * @squareHeight

    drawCollissions: ->

        @context.fillStyle = @fillStyle
        for position in @collissions
            x = position.x * @squareHeight + @position.top
            y = position.y * @squareHeight + @position.left
            @context.fillRect x, y, @squareHeight, @squareHeight

    checkCollissions: (plane1, plane2) ->

        matrix1 = plane1.matrixPosition
        matrix2 = plane2.matrixPosition

        collissions = false

        if matrix1.length and matrix2.length
            for position in matrix1
                for position2 in matrix2
                    if position.x == position2.x and position.y == position2.y
                        collissions = true
                        @collissions.push(position)

        return collissions

window.Collissions = Collissions