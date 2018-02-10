import re, rus, sys, atexit

class _RusGameServer(rus.Server):
    def onmessage(self, event):
        pass

class GameServer:
    def __init__(self):
        self.controllers = {}
        self.controllerIdExpr = re.compile('<\s*controller\s+id\s*=\s*"(\w+)"\s*>')
        self._startServer()
        atexit.register(self._cleanup)

    def _cleanup(self):
        self.cleanup()
        self.server.close()
        print "Game server stopped!"
        sys.exit(0)

    def cleanup(self):
        pass

    def importController(self, filename):
        with open(filename, "r") as f:
            data = f.read()
        id = self.controllerIdExpr.search(data).group(1)
        self.controllers[id] = data

    def switchController(id, players=None):
        if not players:
            _switchController_all(id)
        else:
            if isinstance(players, list):
                _switchController_players(id, players)
            else:
                _switchController_player(id, player)

    def _startServer(self):
        self.server = _RusGameServer(36883)
        cl = rus.Client("localhost", 11026)
        cl.onconnect = lambda: cl.sendr("ready")
        cl.close()

    def _switchController_all(id):
        # todo
        pass

    def _switchController_player(id, player):
        # todo
        pass

    def _switchController_players(id, players):
        # todo
        pass
        
