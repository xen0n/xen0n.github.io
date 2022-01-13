#!/usr/bin/env python3

import glob
import re

FILENAME_RE = re.compile(r'(\d{4})-(\d{2})-(\d{2})-(.*)\.md$')

for filename in glob.iglob('*.md'):
    with open(filename) as fp:
        lines = fp.readlines()

    try:
        draft_line_idx = lines.index('draft: false\n')
    except ValueError:
        # ignore drafts
        continue

    old_style_path = FILENAME_RE.sub(r'/\1/\2/\3/\4/', filename)

    aliases_lines = [
        'aliases:\n',
        f'    - {old_style_path}\n',
    ]

    new_content_lines = lines[:draft_line_idx + 1] + aliases_lines + lines[draft_line_idx + 1:]
    new_content = ''.join(new_content_lines)

    with open(filename, 'w') as fp:
        fp.write(new_content)
