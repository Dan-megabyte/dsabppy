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
            raise NotImplementedError ("Can't decode string yet")
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
            print(str(begin)+" -> "+str(result))
            return (result, (len(begin)-len(bytes)))
        elif bytes[0] <= 0x93:
            raise NotImplementedError ("Can't decode maps yet")
        elif bytes[0] <= 0x96:
            raise NotImplementedError ("Can't decode bytes yet")
        


input = "m8DAzDxhAgMDQ8ML9olAmhFKM4HoiRMB"

input = input.encode("ascii")

input = base64.decodebytes(input)

input = zlib.decompress(input, -15)

print(input)

output = decodeBytes(input)[0]

print(output)