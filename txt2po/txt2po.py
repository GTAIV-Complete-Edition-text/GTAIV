#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from collections import defaultdict
from pathlib import Path
from translate.storage.po import pofile, pounit

def parse_hash_entry(s):
    i = s.find('=')
    if i != -1:
        hash = s[len('0x'):i]
        text = s[i + 1:]
        return (int(hash, base=16), text)

def parse_txt(f):
    name = ''
    table = defaultdict(dict)
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('['):
            i = line.find(']')
            if i != -1:
                name = line[len('['):i]
        elif line.startswith(';0x'):
            hash, text = parse_hash_entry(line[len(';'):])
            table[hash][0] = text
        elif line.startswith('0x'):
            hash, text = parse_hash_entry(line)
            table[hash][1] = text
    return name, table

def text_table2po(name, table):
    po = pofile()
    po.init_headers(project_id_version=name)
    po.settargetlanguage('zh_CN')
    for hash, texts in table.items():
        orig = texts[0]
        translate = texts.get(1, '')
        unit = pounit(source=orig)
        unit.setcontext(format(hash, 'X'))
        unit.target = translate
        po.addunit(unit)
    return po

def text2po(inf, outf):
    name, table = parse_txt(inf)
    po = text_table2po(name, table)
    po.savefile(outf)

if __name__ == '__main__':
    for name in os.listdir('text'):
        path = Path('text', name)
        print(path)
        inf = path.open('r', encoding='utf-8-sig')
        outf = Path('po', path.stem).with_suffix('.po').open('wb')
        text2po(inf, outf)
