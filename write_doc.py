import pathlib

# Content with explicit Unicode escapes for all Chinese characters
lines = []
lines.append('# 数据交接文档 — 爬虫数据入库规范')
lines.append('')
lines.append('## 1. 概述')
lines.append('')
lines.append('本文档面向爬虫项目组，说明爬取的岗位数据需要以何种格式写入数据库，以便后续系统（后端 API、Agent 分析引擎、前端展示）能够正常使用。')
pathlib.Path('F:/lkz/bo/1/codex/my/write_doc.py').write_text(script, 'utf-8')
print('written')
