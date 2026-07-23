path = r'F:\lkz\bo\1\codex\my\agents\agent1\设计框架文档.md'
c = open(path, encoding='utf-8').read()
backslash_n = chr(92) + 'n'
if backslash_n in c:
    c = c.replace(backslash_n, chr(10))
    open(path, 'w', encoding='utf-8').write(c)
    print('fixed newlines')
else:
    print('no literal backslash-n found')
import os
os.remove(__file__)
