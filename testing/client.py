import bs

s = bs.Socket(36883, "localhost")

while True:
    s.send(raw_input())
