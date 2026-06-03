import sys, re
content = sys.stdin.read()
for key in ['roll_failure', 'waitress_bad', 'waitress_init']:
    pattern = '"' + key + '"' + r'\s*:\s*__\((.*?)\),'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        val = m.group(1)[:80]
        print(key, ':', repr(val))
    else:
        print(key, ': NOT FOUND')
