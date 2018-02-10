import atexit

def cleanup():
    print "Cleaning up things before the program exits..."

atexit.register(cleanup)

print "Hello world!"

while True:
    pass