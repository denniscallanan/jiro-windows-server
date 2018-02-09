import thread, datetime, time

def add(ms, func, *args, **kwargs):
    thread.start_new_thread(interval, (func, ms, args, kwargs))

def adds(s, func, *args, **kwargs):
    thread.start_new_thread(interval_seconds, (func, s,args, kwargs))

def interval(func, ms, args, kwargs):
    a = datetime.datetime.now()
    func(*args, **kwargs)
    while True:
        b = datetime.datetime.now()
        dt = (b - a).total_seconds() * 1000
        if dt >= ms:
            func(*args, **kwargs)
            a = b

def interval_seconds(func, s, args, kwargs):
    while True:
        func(*args, **kwargs)
        time.sleep(s)
