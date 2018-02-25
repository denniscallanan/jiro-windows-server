import re, rus, sys, atexit, time
from obj import *
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
            elif event.msg[0] == "e":
                strArgs = event.msg[1:].split("^")
                controllerId = strArgs[0]
                interactId = strArgs[1]
                eventType = strArgs[2]
                if len(strArgs) > 3:
                    eventData = "^".join(strArgs[3:])
                else:
                    eventData = ""
                self.api.controllers[controllerId].interactables[interactId].handleEvent(eventType, eventData, event.addr)
            elif event.msg[0] == "a":
                print "Got message!"
                caretIndex = event.msg.find("^", 1)
                controllerId = event.msg[1:caretIndex]
                eventData = event.msg[caretIndex+1:]
                self.api.controllers[controllerId].handleEvent("accelerometer", eventData, event.addr)
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

    def getController(self, controllerId):
        return self.controllers[controllerId]

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
        time.sleep(0.1)
        # this won't work well if the internet is unreliable
        for id in controller.interactables:
            interactable = controller.interactables[id]
            for eventType in interactable.usedEventTypes:
                self.server.sendr("l" + id + "^" + eventType, player)
        for eventType in controller.usedEventTypes:
            if eventType == "accelerometer":
                print "Sending accelerometer continous data request"
                self.server.sendr("a", player)
        
class _Controller:
    def __init__(self, data, tree, id):
        self.data = data
        self.tree = tree
        self.id = id
        self.interactables = {}
        self.populateInteractables()
        self.eventCallbacks = {}
        self.usedEventTypes = []

    def populateInteractables(self):
        elements = self.tree.findAll(lambda tag: "id" in tag.attrs)
        for el in elements:
            #if "interact" in el.attrs:
            #    interactions = el["interact"].split(" ")
            #else:
            #    interactions = []
            #if el.name == "button":
            #    interactions.append("btn")
            #interactions = list(set(interactions))
            self.interactables[el["id"]] = _Interactable() #_Interactable(interactions)
        if "interact" in self.tree.attrs:
            self.interactables[self.tree["id"]] = _Interactable(list(set(self.tree["interact"].split(" "))))

    def getInteractable(self, interactableId):
        return self.interactables[interactableId]

    def addEventListener(self, eventType, callback):
        if eventType in ["accelerometer"]:
            if eventType not in self.eventCallbacks:
                self.eventCallbacks[eventType] = [callback]
                self.usedEventTypes.append(eventType)
            else:
                self.eventCallbacks[eventType].append(callback)
        else:
            raise Exception("Invalid controller eventType: " + str(eventType))

    def handleEvent(self, eventType, data, addr):
        if eventType in self.eventCallbacks:
            callbacks = self.eventCallbacks[eventType]
            if eventType == "accelerometer":
                x, y, z = map(lambda x: float(x), data.split(","))
                for callback in callbacks:
                    callback(obj(addr=addr, x=x, y=y, z=z))

class _Interactable:
    def __init__(self):
        self.eventCallbacks = {}
        self.usedEventTypes = []

    def addEventListener(self, eventType, callback):
        if eventType in ["tapStart", "tapEnd"]:
            if eventType not in self.eventCallbacks:
                self.eventCallbacks[eventType] = [callback]
                self.usedEventTypes.append(eventType)
            else:
                self.eventCallbacks[eventType].append(callback)
        #tapStart, tapEnd
        else:
            raise Exception("Invalid element eventType: " + str(eventType))

    def handleEvent(self, eventType, data, addr):
        if eventType in self.eventCallbacks:
            callbacks = self.eventCallbacks[eventType]
            if eventType in ["tapStart", "tapEnd"]:
                for callback in callbacks:
                    callback(obj(addr=addr))

def pretty_ip(addr):
    return addr[0].split(".")[-1]+":"+str(addr[1])
