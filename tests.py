import base64
import zlib

from src.dsabppy.dsabppy import encodeList, decodeString

passed = True

tests = {
    "inputlist": [0, 11, 1, [[1, [0, 0, 'config_pusher', 0, [0, 0, 116.5999984741211, 20, False, 8.899999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 9, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 63.400001525878906, 20, False, 8.899999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 1, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 69.4000015258789, 20, False, 8.5], 'filter_items', 0, [0, 0, 0]]], [0, 2, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 58, 20, False, 9.399999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 0, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5224, False, 8.199999809265137], 'filter_items', 0, [0, 0, 0]]], [0, 7, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5196, False, 8.199999809265137], 'filter_items', 0, [0, 0, 0]]], [0, 3, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 82.9000015258789, 20, False, 8.100000381469727], 'filter_items', 0, [0, 0, 0]]], [0, 4, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5210, False, 8], 'filter_items', 0, [0, 0, 0]]], [0, 5, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 110.5999984741211, 20, False, 8.5], 'filter_items', 0, [0, 0, 0]]], [0, 8, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 97.4000015258789, 20, False, 8], 'filter_items', 0, [0, 0, 0]]], [0, 6, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5242, False, 9.399999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 10, 0, 242]]],
    "inputstring": "m8DAzThhAuMUhwkMDF28yfl5aZnp8QWlxRmpRQxAoU4GBoaENLVYB5E+EPPAmTOKDhO7eNIyc0pSi+IzS1Jzi0HKGCZOnDiBgZOh4dNE/GY5GG/2J8osRsJmLZgZGQg1CwjwmMUENcsCu1lWcPco4TaDAWqGJXYzGjMghiSkpSngNoSdgCE+xBjCTEzI7AyBhoyDsTEes1igZhnicFCUSB8HTs2shB2SkLYsmqgo4sAfRdDojnDA5x42AqFbRUw8c4EMmTgRAA==",
    "farmertest": "nVfNbxtFFJ+337v2etfrTVxO5AYScEDhSwgJr1o+bhzgxIGqgriNFNoqDRLHcYilKFKCLXohEu0F8Q/AhSMXTkFcucAhSCWiAaogRCNVSt+bmY0tZWdi+2L/duY3v3nvzXtvdgfswoXBgME8P1j/9+QVNkQ8h/j4ZIGwhdj2ETQRgIdgjkBAtJwf9I5fR5TkJSkvSbkiuS3S+gJIy0MMbQQ+gYQWIrBdomX8L2gRJ+P3eydPIsozfkCaVlNxHATrwByScptIgwWyIsXRhAlj3RRHmzTaSJUhaYrCwtpkjJeUqxsJP5S8pOQ1xniNkpfgKNSIR4AMzRv8kOgx0n0m4uYiBgtBFvP7NFcXc6/RnFMnqQ6iEEd7AHUi1JDwliLUSkKAoxAjiGr80KcQxAhC2jRBIMyAaLStgxjmaGGkgp5Fcv8QSbaUjxADRTEL5VwwJhCUW4M/ZrFfjno+7krbBwTIoLrP/6To4Z94TgmQ5+AJAXFGjlcK5J7KD3DlmTquMtlzy+O2HErAf0SiWLY6Pc9WHvkIeid3ScJC3g8nTwmeVfIsxcstlSwAIp8XkQafE7XN99fDhZCWhW1+L8R/NodjwDiNsWyENxm7U6T8IQ0nfB//2g1+jya63b87Mf9fwmeLmB9L+nsIH0q4Vmz+tHep4L/Q6rpY1q7J1Yy9WuBPXvD/pMIH44+M9cYeWSjXLC7+3AmFdjsQpjB3zGhrDDP+R4ktRs6ygHDA+O89cBDVmHAbbr+B7K34wxvXu8tXL6/cuPLR0iobuBak+c7OcCvuLq+sLa1elvNsYA236mpoeW3p41tssLHM2HBI2gl/RIKXqgSZoxFkZwSZ0ptvGfRcH/W2JzIQlF7NZJ/lTm0fNE32wdR6zrxBD+yJDwQs5a9v0HNsTfzO2lfGL4yk3ttVej5o9OBswqxu3OzvSs34XBunPJOM9BjYBll7hlTMhey8a8ogb2rZFki9F8f1bn5y65rQg34D8p3+ga0vOT/hR6KIX6hUYP3vWL5dpVCeaSviR7T+5akt6H+lJOJESlQGxdOVgb5Mo0AG5c2p2shZPUyx0knHcGzaxDUUQk3qGYJeGTSwXGlPYIrY5J3XK/1rmLKdTdwordK/UOpV3gza6jHcDFFqCBizNt7PtytSbBXKLtFwZMBe0mSpLuCMlQotVyo8LxTOz51HrL/P+keqylL+G91vKf9VGxZ/8kQ/DUuIF1Ko9Qtgc/eJdy/qPFMSKpWemcyv8mqIfIMr4oQny5hTV+LUVGIz9HFVshP6dVoJsfSr+hXEn77vmzqH9h3J0PDn5T3iSVldPuu67iifs5ahhfhsasOa0jBoGa54d7YrPvEN/VyraeznphdD7Y2jd95G53vA9e8hungaWqjJae2bgslpJxYn5ISmuwfObYROJhOn0jCYyTDH5Kqu5kyKdjhbeYwUvJrBSzb5DTtSdJWXz1U1pLMFABZeIfLu8gwtSRtwQ7LiOyN+xltM65+ve7U3nmLLcIre5B8fY1WaScWEFN0r16+uLJFfwgf8sl3o8AcU1xFE9HVhjyB+Et85nXnQwZ+gEI81nHlaQLjdGlff3P3+m4tiByRHBX4uv6NoFUbIPRi7VqnU/fFbqZRs7u19ep7K7pefFaWlC51sBHHmrpzJBVPOdLuDonwcDh8D",
    "dicttestlist": [{1:2, 2:3, 4:5, 3:4}],
}

for test in tests:
    tested = tests[test]
    print("Testing:")
    print(tested)
    if type(tested) == list:
        print("encoding...")
        encoded = encodeList(tested)
        print(encoded)
        print("decoding...")
        test = decodeString(encoded)
        print(test)
        if test == tested:
            print("passed")
        else:
            passed = False
            print("failed")
    elif type(tested) == str:
        print("decoding...")
        decoded =decodeString(tested)
        print(decoded)
        print("encoding...")
        test = encodeList(decoded)
        print(test)
        if test == tested:
            print("passed")
        else:
            passed = False
            print("failed")
        inputBytes = tested.encode("ascii")
        decodedBytes = base64.decodebytes(inputBytes)
        decompressedBytes = zlib.decompress(decodedBytes, -15)
        compressedBytes = zlib.compress(decompressedBytes)[2:-4]
        encodedBytes = base64.encodebytes(compressedBytes)
        test = encodedBytes.decode('ascii').replace("\n", "")
        if test != tested:
            passed = False
            print("failed")
            print(test)

print("ALL TESTS PASSED {}".format(passed))
