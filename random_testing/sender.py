import rus, time

sender = rus.Sender()

while True:
    time.sleep(1)
    sender.send("HelloWorld!", ("localhost", 11026))
