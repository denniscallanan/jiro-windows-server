import re, rus, sys, atexit
#from xml.dom import minidom
from bs4 import BeautifulSoup

class _RusGameServer(rus.Server):
    def __init__(self, api):
        rus.Server.__init__(self, 36883)
        self.players = []
        self.api = api
    def onmessage(self, event):
        if len(event.msg) > 0:
            if event.msg[0] == "j":
                displayName = event.msg[1:]
                self.players.append(event.addr)
                self.api._onPlayerJoin(event.addr)
    def onclientleave(self, event):
        if event.addr in self.players:
            self.players.remove(event.addr)
        self.api._onPlayerLeave(event.addr)

class GameServer:
    def __init__(self):
        atexit.register(self._cleanup)
        self.controllers = {}
        self._startServer()

    def _cleanup(self):
        self.cleanup()
        self.server.close()
        sys.exit(0)

    def cleanup(self):
        pass

    def _onPlayerJoin(self, addr):
        self.onPlayerJoin(addr)

    def onPlayerJoin(self, addr):
        pass

    def _onPlayerLeave(self, addr):
        self.onPlayerLeave(addr)

    def onPlayerLeave(self, addr):
        pass

    def getInteractable(self, controllerId, interactableId):
        return self.controllers[controllerId].interactables[interactableId]

    def importController(self, filename):
        controller = self.createControllerObj(filename)
        self.controllers[controller.id] = controller

    def createControllerObj(self, filename):
        with open(filename, "r") as f:
            data = f.read()
        tree = BeautifulSoup(data, 'lxml').controller
        controller = _Controller(data, tree, tree["id"])
        return controller

    def switchController(self, id, players=None):
        if not players:
            self._switchController_all(id)
        else:
            if isinstance(players, list):
                for player in players:
                    self._switchController_player(id, player)
            else:
                self._switchController_player(id, players)

    def _startServer(self):
        self.server = _RusGameServer(self)
        cl = rus.Client("localhost", 11026)
        #cl.onconnect = lambda: cl.sendr("ready")
        cl.close()

    def _switchController_all(self, id):
        # todo
        pass

    def _switchController_player(self, id, player):
        controller = self.controllers[id]
        self.server.sendr("c" + id + "^" + controller.data.replace("\n", ""), player)
        # this won't work well if the internet is unreliable
        for id in controller.interactables:
            interactable = controller.interactables[id]
            for eventType in interactable.usedEventTypes:
                self.server.sendr("l" + id + "^" + eventType, player)
        
class _Controller:
    def __init__(self, data, tree, id):
        self.data = data
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
        self.eventCallbacks = {}
        self.usedEventTypes = []
    def addEventListener(self, eventType, callback):
        if eventType == "tap":
            if eventType not in self.eventCallbacks:
                self.eventCallbacks[eventType] = [callback]
                self.usedEventTypes.append(eventType)
            else:
                self.eventCallbacks[eventType].append(callback)

        #tapStart, tapEnd
        else:
            raise Exception("Invalid eventType or eventType not part of interactions of that element")

def pretty_ip(addr):
    return addr[0].split(".")[-1]+":"+str(addr[1])
