#!/usr/bin/env python
# coding=utf-8

from collections import Counter
from collections import defaultdict
from generate_item_matchset_from_category_matchset import get_raw_category_match_mapper

class TitleMatchRule:
    def __init__(self):
        pass

    def write_to_file(self, path):
        with open(path, 'w') as f:
            for (item_a, item_b), weight in self.mapper.iteritems():
                f.write("%s %s %d\n" % (item_a, item_b, weight))

    def read_from_file(self, path):
        self.mapper = defaultdict(int)
        with open(path) as f:
            for line in f:
                item_a, item_b, weight = line.strip().split(' ')
                self.mapper[(item_a, item_b)] = int(weight)

    def generate(self, item_detail_file_path, match_list_file_path):
        self.mapper = Counter()
        item_title_mapper = self._generate_item_title_mapper(item_detail_file_path)

        with open(match_list_file_path) as infile:
            for line in infile:
                item_a, match_list = line.strip().split(' ')
                for item_b in match_list.split(','):
                    self._generate_title_match_rule_for_pair(item_a, item_b, item_title_mapper)


    def _generate_item_title_mapper(self, item_detail_file_path):
        mapper = {}
        with open(item_detail_file_path) as f:
            for line in f:
                item_id, _, title = line.strip().split(' ')
                mapper[item_id] = title.split(',')
        return mapper

    def _generate_title_match_rule_for_pair(self, item_a, item_b, item_title_mapper):
        for title_a in item_title_mapper[item_a]:
            for title_b in item_title_mapper[item_b]:
                self.mapper[tuple(sorted([title_a, title_b]))] += 1



if __name__ == '__main__':
    import sys
    item_detail_file = sys.argv[1]
    match_list_file = sys.argv[2]
    rule_file = sys.argv[3]
    rule_obj = TitleMatchRule()
    rule_obj.generate(item_detail_file, match_list_file)
    rule_obj.write_to_file(rule_file)
