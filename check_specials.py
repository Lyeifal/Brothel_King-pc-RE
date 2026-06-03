import sys, re
content = sys.stdin.read()
for key in ['flasher', 'temptress', 'virgin', 'catgirl']:
    pattern = '"' + key + '"' + r'\s*:\s*__\((.*?)\),'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        val = m.group(1)[:120]
        print(key, ':', repr(val))
    else:
        print(key, ': NOT FOUND')
