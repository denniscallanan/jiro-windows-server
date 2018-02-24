import thread, datetime, time

threads = {}
lastid = 0

def add(ms, func, *args, **kwargs):
    global lastid
    lastid += 1
    threads[lastid] = False
    thread.start_new_thread(interval, (func, ms, args, kwargs, lastid))
    return lastid

def adds(s, func, *args, **kwargs):
    global lastid
    lastid += 1
    threads[lastid] = False
    thread.start_new_thread(interval_seconds, (func, s,args, kwargs, lastid))
    return lastid

def stop(id_):
    threads[id_] = True # exit = True

def interval(func, ms, args, kwargs, threadid):
    a = datetime.datetime.now()
    func(*args, **kwargs)
    while True:
        if threads[threadid]:
            del threads[threadid]
            break
        #b = datetime.datetime.now()
        #dt = (b - a).total_seconds() * 1000
        #if dt >= ms:
        #    func(*args, **kwargs)
        #    a = b
        func(*args, **kwargs)
        time.sleep(ms / float(1000))

def interval_seconds(func, s, args, kwargs, threadid):
    while True:
        if threads[threadid]:
            del threads[threadid]
            break
        func(*args, **kwargs)
        time.sleep(s)
