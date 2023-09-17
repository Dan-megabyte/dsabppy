# DSA-blueprints-modifier
A series of python tools to decode, modify, and reencode Deep Space Airships blueprints

Ever wanted to modify/create programaticaly a blueprint?
Well, now you can with this repo

contributions are welcome

## Usage
```python
from dsabppy.dsabppy import encodeList, decodeString

blueprintString = encodeList(["listed data"])

print("DSA:"+blueprintString) # output: "DSA:m9DFnZNZXJKaopCSWJI4EQA="

print(decodeString(blueprintString)[0]) # output: "listed data"
```