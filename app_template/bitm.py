import __builtin__ as _

class Byte:
    def __init__(self, value = 0):
        self._value = value
        self.value_processed = True
        self.bits()

    def chr(self):
        return chr(self.value())

    def bits(self):
        num = self._value
        self.bits = []
        self.bits.append(num % 2)
        while num > 1:
            num /= 2
            self.bits.append(num % 2)

        if len(self.bits) < 8:
            self.bits += [0] * (8 - len(self.bits))
        
        self.bits = list(reversed(self.bits))

    def get(self, index=-1, index2=-1):
        if index == -1:
            return self.bits
        result = 0
        if index2 >= 0:
            for i in range(index2 - index + 1):
                multiplier = 2 ** (index2 - index - i)
                result += self.bits[i + index] * multiplier
            return result
        return self.bits[index]

    def set(self, index, index2, value=None):
        if value == None:
            self.bits[index] = index2 % 2
            return
        bits = []
        bits.append(value % 2)
        while value > 1:
            value /= 2
            bits.append(value % 2)
        if len(bits) <= index2 - index:
            left = (index2 - index - len(bits)) + 1
            bits += [0] * left
        bits = list(reversed(bits))
        self.bits[index:index2+1] = bits
        self.value_processed = False
        
    def value(self):
        if self.value_processed:
            return self._value
        self._value = self.get(0, 7)
        self.value_processed = True
        return self._value

def ord(string):
    nums = [_.ord(char) for char in string]
    result = 0
    for i in range(len(nums)):
        multiplier = 256 ** (len(nums) - i - 1)
        result += nums[i] * multiplier
    return result
    
def chrs(num):
    result = ""
    result += chr(num % 256)
    while num >= 256:
        num /= 256
        result = chr(num % 256) + result
    return result

def tobytes(val):
    if isinstance(val, basestring):
        return tobytes_str(val)
    return tobytes_num(val)

def tobytes_str(string):
    return [Byte(_.ord(char)) for char in string]

def tobytes_num(num):
    nums = []
    nums.insert(0, Byte(num % 256))
    while num > 255:
        num /= 256
        nums.insert(0, Byte(num % 256))
    return nums

def frombytes(byts):
    string = ""
    for byte in byts:
        string += chr(byte.value())
