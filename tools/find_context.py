import subprocess

result = subprocess.run(['git', 'show', 'HEAD:game/BKscreens.rpy'], capture_output=True)
data = result.stdout.decode('utf-8', errors='replace')
lines = data.split('\n')

with open('tools/find_context_output.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(lines):
        if 'girl.get_stat(stat.name) + change' in line:
            out.write(f'Line {i+1}: {line.strip()[:150]}\n')

print('Done. Output in tools/find_context_output.txt')
