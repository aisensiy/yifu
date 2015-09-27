#!/usr/bin/env python
# coding=utf-8

from collections import defaultdict
from collections import Counter
import random
import itertools


def generate_category_item_mapper(filepath):
    mapper = defaultdict(list)
    with open(filepath) as f:
        for line in f:
            item_id, category_id, _ = line.strip().split(' ')
            mapper[category_id].append(item_id)
    print 'total_category:', len(mapper)
    return mapper


def get_raw_category_match_mapper(filepath):
    mapper = defaultdict(list)
    with open(filepath) as f:
        for line in f:
            category, cate_match_list = line.strip().split(' ')
            cate_match_list = cate_match_list.split(',')
            mapper[category] += cate_match_list
            for reverse_cate in cate_match_list:
                mapper[reverse_cate].append(category)
    print 'match category:', len(mapper)
    return mapper


def get_top_n_category_match_mapper(filepath, top_n=200):
    category_match_mapper = get_raw_category_match_mapper(filepath)

    newmapper = {}
    for k, v in category_match_mapper.items():
        match_categories = [[new_k] * (new_v > top_n and top_n or new_v) for new_k, new_v in Counter(v).most_common(3)]
        newmapper[k] = list(itertools.chain.from_iterable(match_categories))
    return newmapper


def generate_matchset(fromfilepath, tofilepath,
                      item_category_mapper, category_item_mapper, category_match_mapper):
    outfile = open(tofilepath, 'w')
    with open(fromfilepath) as infile:
        for idx, line in enumerate(infile):
            item = line.strip()
            category = item_category_mapper[item]
            matched_category_list = category_match_mapper[category]
            matched_item_list = [randompick(category_item_mapper[matched_category])
                                 for matched_category in matched_category_list][:200]
            outfile.write("%s %s\n" % (item, ",".join(matched_item_list)))
            if idx % 100 == 0:
                print idx
    outfile.close()


def randompick(alist):
    return alist[random.randint(0, len(alist) - 1)]


if __name__ == '__main__':
    import sys
    from from_item_to_category import generate_item_category_mapper

    item_detail_file_path = sys.argv[1]
    category_match_file_path = sys.argv[2]
    test_file_path = sys.argv[3]
    result_file_path = sys.argv[4]

    item_category_mapper = generate_item_category_mapper(item_detail_file_path)
    category_item_mapper = generate_category_item_mapper(item_detail_file_path)
    category_match_mapper = get_top_n_category_match_mapper(category_match_file_path)
    generate_matchset(test_file_path, result_file_path,
                      item_category_mapper, category_item_mapper, category_match_mapper)
