"""
替换静态文件, 使用CDN
"""
CDN_VERSION = 1.0

# setting file
from pathlib import Path

cnd_prifex = f'https://cdn.jsdelivr.net/gh/tianyu-su/xpickcn@{CDN_VERSION}/dist/static/'
Path('backend/settings/prod.py').write_text(
    Path('backend/settings/prod.py').read_text(encoding='utf-8').replace('###@@########CND URL PLACEHOLDER ####@@####',
                                                                         f'STATIC_URL = "{cnd_prifex}"'),
    encoding='utf-8')

# replace static files
files = ['dist/index.html', 'dist/static/about.html', 'dist/static/bindpage.html']
for f in files:
    Path(f).write_text(Path(f).read_text(encoding='utf-8').replace('../static/', cnd_prifex),
                       encoding='utf-8')
