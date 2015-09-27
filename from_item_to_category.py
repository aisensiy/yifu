#!/usr/bin/env python
# coding=utf-8

"""
将匹配列表中的 item 换成 category
"""

def generate_item_category_mapper(filepath):
    mapper = {}
    with open(filepath) as f:
        for line in f:
            item_id, category_id, _ = line.strip().split(' ')
            mapper[item_id] = category_id
    return mapper


def replace_item_to_category(fromfilepath, tofilepath, item_category_mapper):
    outfile = open(tofilepath, 'w')
    with open(fromfilepath) as infile:
        for line in infile:
            item, match_list = line.strip().split(' ')
            outfile.write("%s %s\n" % (item_category_mapper[item], \
                                       ",".join(map(lambda x: item_category_mapper[x],
                                                    match_list.split(",")))))


if __name__ == '__main__':
    import sys
    item_detail_file_path = sys.argv[1]
    item_match_file_path = sys.argv[2]
    category_match_file_path = sys.argv[3]
    replace_item_to_category(item_match_file_path,
                             category_match_file_path,
                             generate_item_category_mapper(item_detail_file_path))
