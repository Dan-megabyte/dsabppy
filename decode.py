import base64
import zlib
import codecs

def decodeBytes(bytes:bytes):
    begin = bytes
    bytes = bytes[1:]
    result = []
    while len(bytes) > 0:
        if bytes[0] <= 63:
            result.append(bytes[0])
            bytes = bytes[1:]
        elif bytes[0] <= 127:
            result.append(bytes[0] - 128)
            bytes = bytes[1:]
        elif bytes[0] <= 0x83:
            result.append(
                int(
                codecs.encode(
                bytes[1:(
                bytes[0]-126
                )], 'hex'), 16))
            bytes = bytes[(bytes[0]-126):]
        elif bytes[0] <= 0x87:
            raise NotImplementedError ("Can't decode signed int yet")
        elif bytes[0] <= 0x89:
            raise NotImplementedError ("Can't decode float yet")
        elif bytes[0] <= 0x8C:
            if bytes[0] == 0x8a:
                length = bytes[1]*16**0
                result.append(bytes[2:(length+2)].decode('utf8'))
                bytes = bytes[length+2:]
            if bytes[0] == 0x8b:
                length = bytes[1]*16**1+bytes[2]*16**0
                result.append(bytes[3:(length+3)].decode('utf8'))
                bytes = bytes[length+3:]
            if bytes[0] == 0x8c:
                length = bytes[1]*16**3+bytes[2]*16**2+bytes[3]*16**1+bytes[4]*16**0
                result.append(bytes[5:(length+5)].decode('utf8'))
                bytes = bytes[length+5:]
        elif bytes[0] <= 0x8F:
            if bytes[0] == 0x8D:
                result.append(True)
            if bytes[0] == 0x8E:
                result.append(False)
            if bytes[0] == 0x8F:
                result.append(None)
            bytes = bytes[1:]
        elif bytes[0] == 0x90:
            decodedbytes = decodeBytes(bytes)
            result.append(decodedbytes[0])
            bytes = bytes[decodedbytes[1]:]
        elif bytes[0] == 0x91:
            bytes = bytes[1:]
            return (result, (len(begin)-len(bytes)))
        elif bytes[0] <= 0x93:
            raise NotImplementedError ("Can't decode maps yet")
        elif bytes[0] <= 0x96:
            if bytes[0] == 0x94:
                result.append(bytes[1:2])
                bytes = bytes[2:]
            elif bytes[0] == 0x95:
                result.append(bytes[1:3])
                bytes = bytes[3:]
            elif bytes[0] == 0x96:
                result.append(bytes[1:5])
                bytes = bytes[5:]
        else:
            raise NotImplementedError ("Can't decode byte "+str(bytes[0]))
        


input = "LYlBCoAgFAXfp5YJLTpS95AoDcESzAO0For/oeO2yKjVDDMMIma6egayGsNq3ax9GCYTwVVNbXeckpV1Ppmovw+G5OZPLpllKwUQkRf7XeQB"

input = input.encode("ascii")

input = base64.decodebytes(input)

input = zlib.decompress(input, -15)

print(input)

output = decodeBytes(input)[0]

print(output)