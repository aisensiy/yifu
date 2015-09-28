#!/usr/bin/env python
# coding=utf-8

from collections import defaultdict
from collections import Counter
from title_match_rule import TitleMatchRule
from category_match_rule import CategoryMatchRule
from commons import *

class TitleScorer:
    def __init__(self, item_title_mapper):
        rule = TitleMatchRule()
        print 'read title match rules...'
        rule.read_from_file('rules/title_match_rules.txt')
        self.title_rules = rule.mapper
        self.item_title_mapper = item_title_mapper

    def score(self, item_a, item_b):
        item_a_title_set = self.item_title_mapper[item_a]
        item_b_title_set = self.item_title_mapper[item_b]
        return sum(self.title_rules[tuple(sorted([title_a, title_b]))]
                   for title_a in item_a_title_set for title_b in item_b_title_set)



class ItemFilter:
    def __init__(self, match_category_mapper, category_item_mapper, item_category_mapper):
        self.match_category_mapper = self._get_pure_mapper(match_category_mapper)
        self.category_item_mapper = category_item_mapper
        self.item_category_mapper = item_category_mapper

    def get_candidates(self, item_a):
        category_a = self.item_category_mapper[item_a]
        for match_category in self.match_category_mapper[category_a]:
            for item_b in self.category_item_mapper[match_category][:100]:
                yield(item_b)

    def _get_pure_mapper(self, match_category_mapper):
        newmapper = defaultdict(set)
        for category_a, category_b in match_category_mapper:
            newmapper[category_a].add(category_b)
        return newmapper
        

def process(test_file_path, result_file_path):
    n = 10
    cate_rule = CategoryMatchRule()
    cate_rule.read_from_file('rules/category_match_rules.txt')
    item_filter = ItemFilter(cate_rule.mapper, generate_category_item_mapper('data/dim_items.txt'), generate_item_category_mapper('data/dim_items.txt'))
    title_scorer = TitleScorer(generate_item_title_mapper('data/dim_items.txt'))
    outfile = open(result_file_path, 'w')
    print 'start generate result...'
    with open(test_file_path) as infile:
        for idx, line in enumerate(infile):
            item_a = line.strip()
            mapper = Counter()
            for item_b in item_filter.get_candidates(item_a):
                mapper[item_b] = title_scorer.score(item_a, item_b)
            print '[', idx, ']'
            outfile.write("%s %s\n" % (item_a,
                                       ",".join(map(lambda x: x[0],
                                                    mapper.most_common(n)))))
    outfile.close()


if __name__ == '__main__':
    import sys
    process(sys.argv[1], sys.argv[2])
