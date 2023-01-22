import base64
import zlib
import codecs
import struct

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
            length = len(data)
            if length <= 0xFF:
                output += b'\x8a'
                output += length.to_bytes(1, "little")
            elif length <= 0xFFFF:
                output += b'\x8b'
                output += length.to_bytes(2, "little")
            elif length <= 0xFFFFFFFF:
                output += b'\x8c'
                output += length.to_bytes(4, "little")
            else:
                raise OverflowError ("String ["+data+"] too long to represent (length>0xFFFFFFFF)")
            output += data.encode('utf8')
        elif type(data) == list:
            output += encodeBytes(data)
        elif type(data) == float:
            output += b'\x89'
            output += struct.pack("d", data)
        elif type(data) == bytes:
            length = len(data)
            if length <= 0xFF:
                output += b'\x94'
                output += length.to_bytes(1, "little")
            elif length <= 0xFFFF:
                output += b'\x95'
                output += length.to_bytes(2, "little")
            elif length <= 0xFFFFFFFF:
                output += b'\x96'
                output += length.to_bytes(4, "little")
            else:
                raise OverflowError ("Bytes "+data+" too long to be represented")
            output += data
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

inputList = [0, 11, 1, [[1, [0, 0, 'config_pusher', 0, [0, 0, 116.5999984741211, 20, False, 8.899999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 9, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 63.400001525878906, 20, False, 8.899999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 1, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 69.4000015258789, 20, False, 8.5], 'filter_items', 0, [0, 0, 0]]], [0, 2, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 58, 20, False, 9.399999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 0, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5224, False, 8.199999809265137], 'filter_items', 0, [0, 0, 0]]], [0, 7, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5196, False, 8.199999809265137], 'filter_items', 0, [0, 0, 0]]], [0, 3, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 82.9000015258789, 20, False, 8.100000381469727], 'filter_items', 0, [0, 0, 0]]], [0, 4, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5210, False, 8], 'filter_items', 0, [0, 0, 0]]], [0, 5, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 110.5999984741211, 20, False, 8.5], 'filter_items', 0, [0, 0, 0]]], [0, 8, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 97.4000015258789, 20, False, 8], 'filter_items', 0, [0, 0, 0]]], [0, 6, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5242, False, 9.399999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 10, 0, 242]]]

for i in range(len(inputList[3])):
    command = inputList[3][i]
    if command[0] == 1:
        commandbytes = encodeBytes(command[1])#[1:-1]
        inputList[3][i][1] = commandbytes

print(inputList)

inputbytes = encodeBytes(inputList)

output = zlib.compress(inputbytes)[2:-4]

output = base64.encodebytes(output)

output = output.decode('ascii').replace("\n", "")

print(output)