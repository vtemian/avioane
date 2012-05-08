#set up the war
class War

  constructor: (opts) ->
    @user = opts.user
    @battleId = opts.battleId
    @userSocket = opts.userSocket

    @mapCanvas = opts.mapCanvas

    @sendData "test", "testing"

  sendData: (event, message) ->
    @userSocket.emit event, message

window.War = War