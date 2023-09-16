import base64
import zlib
import struct

def _encodeBytes(datalist:list, /, float_precision:str="single") -> bytes:
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
                    output += struct.pack("<h", data)
                elif data >= -0x7FFFFF:
                    output += b'\x85'
                    output += struct.pack("<i", data)
                elif data >= -0x7FFFFFFF:
                    output += b'\x86'
                    output += struct.pack("<l", data)
                elif data >= -0x7FFFFFFFFF:
                    output += b'\x87'
                    output += struct.pack("<q", data)
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
            output += _encodeBytes(data)
        elif type(data) == float:
            if float_precision == "single":
                output += b'\x88'
                output += struct.pack("<f", data)
            elif float_precision == "double":
                output += b'\x89'
                output += struct.pack("<d", data)
            else:
                raise RuntimeError ("float_precision must be 'single' or 'double'")
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
        elif type(data) == dict:
            output += b'\x92'
            temp = []
            for key in data:
                temp.append(key)
                temp.append(data[key])
            output += _encodeBytes(temp)[1:-1]
            del temp
            output += b'\x93'
        else:
            raise NotImplementedError (str(type(data))+" byte encoding isn't implemented yet")
    return output + b'\x91'

def encodeList(inputList:list, /, configMessageEnabled:bool=False) -> str:
    if configMessageEnabled:
        for i in range(len(inputList[3])):
            command = inputList[3][i]
            if command[0] == 1:
                commandbytes = _encodeBytes(command[1])#[1:-1]
                inputList[3][i][1] = commandbytes

    #print(inputList)

    inputbytes = _encodeBytes(inputList)
    print(inputbytes)
    compressedBytes = zlib.compress(inputbytes)[2:-4]

    encodedBytes = base64.encodebytes(compressedBytes)

    output = encodedBytes.decode('ascii').replace("\n", "")

    #print(output)
    return output