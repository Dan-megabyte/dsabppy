import base64
import zlib
import codecs

inputbytes = b'\x90\x00\x03\x03\x90\x90\x00\x00\x02\x80\xe8\x07\x91\x90\x00\x00\x01\x80\xe8\x07\x91\x90\x00\x00\x00\x80\xe8\x07\x91\x91\x91'

def encodeBytes(list:list) -> bytes:
    output = b'\x90'
    for data in list:
        if type(data) == int:
            if data == 0:
                output += b'\x00'
            elif data > 0:
                if data < 64:
                    output += data.to_bytes()
                if data >= 64:
                    
            elif data < 0:
                if data >= -64:
    return output + b'\x91'

output = zlib.compress(inputbytes)[2:-4]

output = base64.encodebytes(output)

output = output.decode('ascii')

print(output)