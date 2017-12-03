import bitmanip

o = bitmanip.ord("ab")
print o
print bitmanip.chrs(o)

byts = bitmanip.tobytes("ab")
print byts

for byte in byts:
    print "Value:", byte.value
    print "All bits:", byte.bits()
    print "Bit 0 to 3:", byte.bits(0, 3)
