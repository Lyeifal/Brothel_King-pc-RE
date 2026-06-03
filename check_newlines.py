import re

with open(r'C:\Users\akxls\Documents\Code\BK\Brothel_King-pc\game\tl\chinese_simplified\strings.rpy', 'r', encoding='utf-8') as f:
    content = f.read()

p = re.compile(r'^\s+old\s+"((?:[^"\\]|\\.)*)"\s*\n^\s+new\s+"((?:[^"\\]|\\.)*)"\s*\n', re.MULTILINE)
count = 0
for m in p.finditer(content):
    old_text = m.group(1).replace('\\"', '"').replace('\\\\', '\\')
    new_text = m.group(2).replace('\\"', '"').replace('\\\\', '\\')
    if '\n' in new_text and '\n' not in old_text:
        count += 1
        if count <= 5:
            print('OLD:', repr(old_text[:80]))
            print('NEW:', repr(new_text[:80]))
            print('---')

print('Total new with extra newline:', count)
