import re, rus, sys, atexit
#from xml.dom import minidom
from bs4 import BeautifulSoup

class _RusGameServer(rus.Server):
    def onmessage(self, event):
        pass

class GameServer:
    def __init__(self):
        atexit.register(self._cleanup)
        self.controllers = {}
        #self.controllerIdExpr = re.compile('<\s*controller\s+id\s*=\s*"(\w+)"\s*>')
        self._startServer()

    def _cleanup(self):
        self.cleanup()
        self.server.close()
        print "Game server stopped!"
        sys.exit(0)

    def cleanup(self):
        pass

    def importController(self, filename):
        #id = self.controllerIdExpr.search(data).group(1)
        controller = self.createControllerObj(filename)
        self.controllers[controller.id] = controller

    def createControllerObj(self, filename):
        with open(filename, "r") as f:
            data = f.read()
        tree = BeautifulSoup(data, 'lxml').controller
        controller = _Controller(tree, tree["id"])
        return controller

    def switchController(id, players=None):
        if not players:
            _switchController_all(id)
        else:
            if isinstance(players, list):
                for player in players:
                 _switchController_player(id, player)
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
        
class _Controller:
    def __init__(self, tree, id):
        self.tree = tree
        self.id = id
        self.interactables = {}
        self.populateInteractables()

    def populateInteractables(self):
        elements = self.tree.findAll(lambda tag: "id" in tag.attrs)
        for el in elements:
            if "interact" in el.attrs:
                interactions = el["interact"].split(" ")
            else:
                interactions = []
            if el.name == "button":
                interactions.append("btn")
            interactions = list(set(interactions))
            self.interactables[el["id"]] = _Interactable(interactions)
        if "interact" in self.tree.attrs:
            self.interactables[self.tree["id"]] = _Interactable(list(set(self.tree["interact"].split(" "))))

class _Interactable:
    def __init__(self, interactions):
        self.interactions = interactions