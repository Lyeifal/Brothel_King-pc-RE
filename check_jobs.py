import sys, re
content = sys.stdin.read()
for key in ['waitress_very bad', 'waitress_bad', 'waitress_average', 'waitress_good']:
    pattern = '"' + key + '"' + r'\s*:\s*__\((.*?)\),'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        val = m.group(1)[:120]
        print(key, ':', repr(val))
    else:
        print(key, ': NOT FOUND')
