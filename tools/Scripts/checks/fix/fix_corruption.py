with open('game/core/ui/screens.rpy', 'rb') as f:
    data = f.read()

# Search for all occurrences of byte e9 89 83
idx = 0
count = 0
while True:
    idx = data.find(b'\xe9\x89\x83', idx)
    if idx < 0:
        break
    count += 1
    start = max(0, idx - 30)
    end = min(len(data), idx + 50)
    print(f'Found at byte {idx}: {data[start:end]}')
    idx += 1

print(f'Total occurrences: {count}')
