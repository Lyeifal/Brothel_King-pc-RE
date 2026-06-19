with open('game/core/ui/screens.rpy', 'rb') as f:
    data = f.read()

# Search for the byte sequence e9 89 83
needle = bytes([0xe9, 0x89, 0x83])
idx = data.find(needle)
if idx >= 0:
    start = max(0, idx - 50)
    end = min(len(data), idx + 100)
    print(f'Found at byte offset {idx}')
    print(f'Context: {data[start:end]}')
    print(f'Context hex: {data[start:end].hex()}')
else:
    print('Byte sequence not found')
