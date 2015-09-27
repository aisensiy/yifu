#!/usr/bin/env python
# coding=utf-8

"""
将搭配列表转换成预测结果的形式
"""

from collections import defaultdict

def process(fromfile, tofile):
    outfile = open(tofile, 'w')
    with open(fromfile) as infile:
        for line in infile:
            id, match = line.strip().split(' ')
            match_list = [items_str.split(",") for items_str in match.split(";")]
            write_list(match_list, outfile)
    outfile.close()


def write_list(match_list, outfile):
    mapper = defaultdict(set)
    for i in range(len(match_list)):
        for item1 in match_list[i]:
            for k in range(i + 1, len(match_list)):
                for item2 in match_list[k]:
                    mapper[item1].add(item2)
    for k, v in mapper.items():
        outfile.write("%s %s\n" % (k, ",".join(v)))


if __name__ == '__main__':
    import sys
    fromfile = sys.argv[1]
    tofile = sys.argv[2]
    process(fromfile, tofile)
