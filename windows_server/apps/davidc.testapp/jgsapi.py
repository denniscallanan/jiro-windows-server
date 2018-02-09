import re, rus

class _RusGameServer(rus.Server):
    def onmessage(self, event):
        if event.msg == "TEMP_EXIT":
            print "[TEMP_EXIT] Exiting app..."
            exit(1)

class GameServer:
    def __init__(self):
        self.controllers = {}
        self.controllerIdExpr = re.compile('<\s*controller\s+id\s*=\s*"(\w+)"\s*>')
        self._startServer()

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

    def _switchController_all(id):
        # todo
        pass

    def _switchController_player(id, player):
        # todo
        pass

    def _switchController_players(id, players):
        # todo
        pass
        
