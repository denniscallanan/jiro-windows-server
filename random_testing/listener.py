import rus

class Listener(rus.Listener):
    def onmessage(self, event):
        print event.msg

Listener("localhost", 11026)
rus.keepWindowOpen()
