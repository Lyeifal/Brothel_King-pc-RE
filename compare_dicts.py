import sys, re

# Read stdin
content = sys.stdin.read()

# Find perform_job_dict
m = re.search(r'perform_job_dict\s*=\s*\{', content)
if m:
    start = m.start()
    brace_count = 0
    end = start
    for i in range(start, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break
    dict_text = content[start:end]
    # Count strings with \n
    matches = re.findall(r'"[^"]*\\n[^"]*"', dict_text)
    print('Strings with backslash-n:', len(matches))
    for m in matches[:5]:
        print('  ', m[:100])
else:
    print('perform_job_dict not found')
