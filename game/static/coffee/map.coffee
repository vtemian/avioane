#Map object
class Map
    constructor:(opts) ->
        @context = opts.context
        @position = opts.position
        @squareHeight = opts.squareHeight

        @format = 9

        @fillStyle = "#000"
        @strokeStyle = "red"
        @strokeWidth = 2

        @width = (@format+1) * @squareHeight
        @height = (@format+1) * @squareHeight

        @draw()

    draw: ->

        @context.fillStyle = @fillStyle
        @context.strokeStyle = @strokeStyle
        @context.lineWidth = @strokeWidth

        for line in [0..@format]
            for column in [0..@format]
                x = line * @squareHeight + @position.left
                y = column * @squareHeight + @position.top
                @context.beginPath()
                @context.rect x, y, @squareHeight, @squareHeight
                @context.fill()
                @context.stroke()

window.Map = Map