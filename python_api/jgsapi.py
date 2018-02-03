import re

class GameServer:
    def __init__(self):
        self.controllers = {}
        self.controllerIdExpr = re.compile('<\s*controller\s+id\s*=\s*"(\w+)"\s*>')

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

    def _switchController_all(id):
        # todo
        pass

    def _switchController_player(id, player):
        # todo
        pass

    def _switchController_players(id, players):
        # todo
        pass
        