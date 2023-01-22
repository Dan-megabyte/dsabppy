import base64
import zlib
import codecs
import struct

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
            length = bytes[0]-0x7E
            result.append(
                int(
                codecs.encode(bytes[1:(length)], 'hex'),
                16,))
            bytes = bytes[length:]
        elif bytes[0] <= 0x87:
            if bytes[0] == 0x84:
                result.append(struct.unpack('h', bytes[1:3])[0])
                bytes = bytes[3:]
            if bytes[0] == 0x85:
                result.append(struct.unpack('i', bytes[1:5])[0])
                bytes = bytes[5:]
            if bytes[0] == 0x86:
                result.append(struct.unpack('l', bytes[1:9])[0])
                bytes = bytes[9:]
            if bytes[0] == 0x87:
                result.append(struct.unpack('q', bytes[1:17])[0])
                bytes = bytes[17:]
        elif bytes[0] <= 0x89:
            if bytes[0] == 0x88:
                result.append(struct.unpack('f', bytes[1:5])[0])
                bytes = bytes[5:]
            if bytes[0] == 0x89:
                result.append(struct.unpack('d', bytes[1:9])[0])
                bytes = bytes[8:]
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
        


input = "hdE7CsJAEAbgWeMjPqvgPWQVxM7UnsAmhWRNwBdJbATBwiKkCLtgk/RexFqP4AFsPYFZSZndaXf5P/6Z4dAlnJPblAMk/dV+x/y1cziGnhtA8RRT+rGtNGZsMBdJj/mbyA0cP3K3ofwGIQSHNly+QmPk2Rk1CGK8nok0AEy1USuNcbUx+3cYqvNQ5ifV+atXAJQaaqCFAAsMMNAt3OUW8oyojXppjBQlllZqKsMNpAClb/QMpv4MxRAPW9ehiWzxhN2xIwEhfg=="

input = input.encode("ascii")

input = base64.decodebytes(input)

input = zlib.decompress(input, -15)

print(input)

output = decodeBytes(input)[0]

print(output)

for i in range(len(output[3])):
    command = output[3][i]
    if command[0] == 1:
        output[3][i][1] = decodeBytes(command[1])[0]

print(output)