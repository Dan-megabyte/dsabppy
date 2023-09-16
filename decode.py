import base64
import zlib
import struct

def _decodeBytes(bytes:bytes) -> list:
    begin = bytes
    bytes = bytes[1:]
    result = []
    while len(bytes) > 0:
        if bytes[0] <= 0x3F:
            result.append(bytes[0])
            bytes = bytes[1:]
        elif bytes[0] <= 0x7F:
            result.append((bytes[0] - 0x3F) * -1)
            bytes = bytes[1:]
        elif bytes[0] <= 0x83:
            length = bytes[0]-0x7E
            result.append(int.from_bytes(bytes[1:(length)], 'little'))
            bytes = bytes[length:]
        elif bytes[0] <= 0x87:
            if bytes[0] == 0x84:
                result.append(struct.unpack('h', bytes[1:3])[0])
                bytes = bytes[3:]
            if bytes[0] == 0x85:
                result.append(struct.unpack('i', bytes[1:5])[0])
                bytes = bytes[5:]
            if bytes[0] == 0x86:
                result.append(struct.unpack('l', bytes[1:7])[0])
                bytes = bytes[7:]
            if bytes[0] == 0x87:
                result.append(struct.unpack('q', bytes[1:9])[0])
                bytes = bytes[9:]
        elif bytes[0] <= 0x89:
            if bytes[0] == 0x88:
                result.append(struct.unpack('f', bytes[1:5])[0])
                bytes = bytes[5:]
            if bytes[0] == 0x89:
                result.append(struct.unpack('d', bytes[1:9])[0])
                bytes = bytes[9:]
        elif bytes[0] <= 0x8C:
            if bytes[0] == 0x8a:
                length = bytes[1]*16**0
                result.append(bytes[2:(length+2)].decode('utf8'))
                bytes = bytes[length+2:]
            elif bytes[0] == 0x8b:
                length = bytes[1]*16**1+bytes[2]*16**0
                result.append(bytes[3:(length+3)].decode('utf8'))
                bytes = bytes[length+3:]
            elif bytes[0] == 0x8c:
                length = bytes[1]*16**3+bytes[2]*16**2+bytes[3]*16**1+bytes[4]*16**0
                result.append(bytes[5:(length+5)].decode('utf8'))
                bytes = bytes[length+5:]
        elif bytes[0] <= 0x8F:
            if bytes[0] == 0x8D:
                result.append(True)
            elif bytes[0] == 0x8E:
                result.append(False)
            elif bytes[0] == 0x8F:
                result.append(None)
            bytes = bytes[1:]
        elif bytes[0] == 0x90: #start of an array
            decodedbytes = _decodeBytes(bytes)
            result.append(decodedbytes[0])
            bytes = bytes[decodedbytes[1]:]
        elif bytes[0] == 0x91: #end of an array
            bytes = bytes[1:]
            return (result, (len(begin)-len(bytes)))
        elif bytes[0] == 0x92: #start of a map
            decodedbytes = _decodeBytes(bytes)
            if len(decodedbytes) % 2 == 1:
                raise ValueError ("Map {} has an odd number of objects".format(decodedbytes))
            obj_map = {}
            for i in range(0, len(decodedbytes), 2):
                obj_map[decodedbytes[i]] = decodedbytes[i+1]
            result.append(obj_map)
            del obj_map
        elif bytes[0] == 0x93: #end of a map
            bytes = bytes[1:]
            return (result, (len(begin)-len(bytes)))
        elif bytes[0] <= 0x96: #arbitrary bytes
            if bytes[0] == 0x94:
                length = bytes[1]*16**0
                result.append(bytes[2:(length+2)])
                bytes = bytes[length+2:]
            elif bytes[0] == 0x95:
                length = bytes[1]*16**1+bytes[2]*16**0
                result.append(bytes[3:(length+3)])
                bytes = bytes[length+3:]
            elif bytes[0] == 0x96:
                length = bytes[1]*16**3+bytes[2]*16**2+bytes[3]*16**1+bytes[4]*16**0
                result.append(bytes[5:(length+5)])
                bytes = bytes[length+5:]
        else:
            raise NotImplementedError ("Can't decode byte "+str(bytes[0]))
        


input = "m8DAzThhAuMUhwkMDF28yfl5aZnp8QWlxRmpRQxAoU4GBoaENLVYB5E+EPPAmTOKDhO7eNIyc0pSi+IzS1Jzi0HKGCZOnDiBgZOh4dNE/GY5GG/2J8osRsJmLZgZGQg1CwjwmMUENcsCu1lWcPco4TaDAWqGJXYzGjMghiSkpSngNoSdgCE+xBjCTEzI7AyBhoyDsTEes1igZhnicFCUSB8HTs2shB2SkLYsmqgo4sAfRdDojnDA5x42AqFbRUw8c4EMmTgRAA=="

def decodeString(inputString:str, /, configMessageEnabled:bool=False) -> list:
    inputBytes = inputString.encode("ascii")
    decodedBytes = base64.decodebytes(inputBytes)
    decompressedBytes = zlib.decompress(decodedBytes, -15)
    #print(decompressedBytes)
    output = _decodeBytes(decompressedBytes)[0]
    #print(output)
    if configMessageEnabled:
        for i in range(len(output[3])):
            command = output[3][i]
            if command[0] == 1:
                output[3][i][1] = _decodeBytes(command[1])[0]
    #print(output)
    return output