import rus

class Listener(rus.Listener):
    def onmessage(self, event):
        print event.msg

Listener("", 11026)
rus.keepWindowOpen()
