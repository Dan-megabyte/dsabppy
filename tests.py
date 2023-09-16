from decode import decodeString
from encode import encodeList

passed = True

inputlist = [0, 11, 1, [[1, [0, 0, 'config_pusher', 0, [0, 0, 116.5999984741211, 20, False, 8.899999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 9, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 63.400001525878906, 20, False, 8.899999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 1, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 69.4000015258789, 20, False, 8.5], 'filter_items', 0, [0, 0, 0]]], [0, 2, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 58, 20, False, 9.399999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 0, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5224, False, 8.199999809265137], 'filter_items', 0, [0, 0, 0]]], [0, 7, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5196, False, 8.199999809265137], 'filter_items', 0, [0, 0, 0]]], [0, 3, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 82.9000015258789, 20, False, 8.100000381469727], 'filter_items', 0, [0, 0, 0]]], [0, 4, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5210, False, 8], 'filter_items', 0, [0, 0, 0]]], [0, 5, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 110.5999984741211, 20, False, 8.5], 'filter_items', 0, [0, 0, 0]]], [0, 8, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 97.4000015258789, 20, False, 8], 'filter_items', 0, [0, 0, 0]]], [0, 6, 0, 242], [1, [0, 0, 'config_pusher', 0, [0, 0, 5242, False, 9.399999618530273], 'filter_items', 0, [0, 0, 0]]], [0, 10, 0, 242]]]
inputstring = "m8DAzThhAuMUhwkMDF28yfl5aZnp8QWlxRmpRQxAoU4GBoaENLVYB5E+EPPAmTOKDhO7eNIyc0pSi+IzS1Jzi0HKGCZOnDiBgZOh4dNE/GY5GG/2J8osRsJmLZgZGQg1CwjwmMUENcsCu1lWcPco4TaDAWqGJXYzGjMghiSkpSngNoSdgCE+xBjCTEzI7AyBhoyDsTEes1igZhnicFCUSB8HTs2shB2SkLYsmqgo4sAfRdDojnDA5x42AqFbRUw8c4EMmTgRAA=="

tested = inputlist

print("Testing:")
print(tested)
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
    
tested = inputstring
print("Testing:")
print(tested)
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


print("ALL TESTS PASSED {}".format(passed))
