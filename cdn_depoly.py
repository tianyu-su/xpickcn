"""
替换静态文件, 使用CDN
"""
import argparse

# setting file
from pathlib import Path


def main(cnd_version):
    cnd_prefix = f'https://cdn.jsdelivr.net/gh/tianyu-su/xpickcn@{cnd_version}/dist/static/'
    Path('backend/settings/prod.py').write_text(
        Path('backend/settings/prod.py').read_text(encoding='utf-8').replace(
            '###@@########CND URL PLACEHOLDER ####@@####',
            f'STATIC_URL = "{cnd_prefix}"'),
        encoding='utf-8')

    # replace static files
    files = ['dist/index.html', 'dist/static/about.html', 'dist/static/bindpage.html']
    for f in files:
        Path(f).write_text(Path(f).read_text(encoding='utf-8').replace('../static/', cnd_prefix),
                           encoding='utf-8')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('tag_version', type=str, help='release version for cdn')
    args = parser.parse_args()
    main(args.tag_version)

