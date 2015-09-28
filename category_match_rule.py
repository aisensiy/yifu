#!/usr/bin/env python
# coding=utf-8

from collections import Counter
from generate_item_matchset_from_category_matchset import get_raw_category_match_mapper

class CategoryMatchRule:
    def __init__(self):
        pass

    def write_to_file(self, path):
        with open(path, 'w') as f:
            for (item_a, item_b), weight in self.mapper.iteritems():
                f.write("%s %s %d\n" % (item_a, item_b, weight))

    def read_from_file(self, path):
        self.mapper = {}
        with open(path) as f:
            for line in f:
                item_a, item_b, weight = line.strip().split(' ')
                self.mapper[(item_a, item_b)] = int(weight)

    def generate(self, filepath):
        raw_mapper = get_raw_category_match_mapper(filepath)
        counter_mapper = {}
        for k, v in raw_mapper.items():
            counter_mapper[k] = Counter(v)

        pair_mapper = Counter()
        for item_a, v in counter_mapper.iteritems():
            for item_b, weight in v.items():
                pair_mapper[tuple(sorted([item_a, item_b]))] += weight

        self.mapper = pair_mapper


if __name__ == '__main__':
    import sys
    raw_category_match_file = sys.argv[1]
    pure_category_match_file = sys.argv[2]
    rule_obj = CategoryMatchRule()
    rule_obj.generate(raw_category_match_file)
    rule_obj.write_to_file(pure_category_match_file)
