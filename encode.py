import base64
import zlib
import codecs
import struct

inputbytes = b'\x90\x00\x03\x03\x90\x90\x00\x00\x00\x80\xe8\x07\x91\x90\x00\x00\x01\x80\xe8\x07\x91\x90\x00\x00\x02\x80\xe8\x07\x91\x91\x91'

def encodeBytes(datalist:list) -> bytes:
    output = b'\x90'
    for data in datalist:
        if type(data) == int:
            if data == 0:
                output += b'\x00'
            elif data > 0:
                if data < 64:
                    output += data.to_bytes(1, "little")
                elif data <= 0xFF:
                    output += b'\x80'
                    output += data.to_bytes(1, "little")
                elif data <= 0xFFFF:
                    output += b'\x81'
                    output += data.to_bytes(2, "little")
                elif data <= 0xFFFFFF:
                    output += b'\x82'
                    output += data.to_bytes(3, "little")
                elif data <= 0xFFFFFFFF:
                    output += b'\x83'
                    output += data.to_bytes(4, "little")
                else:
                    raise OverflowError ("Unsigned Int: "+int(data)+" too big to represent (greater than 4294967295)")
            elif data < 0:
                if data >= -64:
                    data = data * (-1) + 0x3f
                    output += data.to_bytes(1, "little")
                elif data >= -0x7FFF:
                    output += b'\x84'
                    output += struct.pack("h", data)
                elif data >= -0x7FFFFF:
                    output += b'\x85'
                    output += struct.pack("i", data)
                elif data >= -0x7FFFFFFF:
                    output += b'\x86'
                    output += struct.pack("l", data)
                elif data >= -0x7FFFFFFFFF:
                    output += b'\x87'
                    output += struct.pack("q", data)
                else:
                    raise OverflowError ("Negative Signed Int: "+int(data)+" too big to represent (smaller than 0x7FFFFFFFFF)")
        elif type(data) == str:
            raise NotImplementedError ("String byte encoding isn't implemented yet")
        elif type(data) == list:
            output += encodeBytes(data)
        elif type(data) == bool:
            if data == True:
                output += b'\x8D'
            elif data == False:
                output += b'\x8E'
        elif data == None:
            output += b'\x8F'
        else:
            raise NotImplementedError (str(type(data))+" byte encoding isn't implemented yet")
    return output + b'\x91'

inputList = [0, 3, 3, [[0, 0, 0, 232, 7], [0, 0, 1, 232, 7], [0, 0, 2, 232, 7]]]

inputbytes = encodeBytes(inputList)

output = zlib.compress(inputbytes)[2:-4]

output = base64.encodebytes(output)

output = output.decode('ascii')

print(output)