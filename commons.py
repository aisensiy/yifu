#!/usr/bin/env python
# coding=utf-8

from collections import defaultdict


def generate_item_category_mapper(filepath):
    print 'generate item cate mapper...'
    mapper = {}
    with open(filepath) as f:
        for line in f:
            item_id, category_id, _ = line.strip().split(' ')
            mapper[item_id] = category_id
    return mapper


def generate_category_item_mapper(filepath):
    print 'generate cate item mapper...'
    mapper = defaultdict(list)
    with open(filepath) as f:
        for line in f:
            item_id, category_id, _ = line.strip().split(' ')
            mapper[category_id].append(item_id)
    return mapper


def generate_item_title_mapper(filepath):
    print 'generate item title mapper...'
    mapper = {}
    with open(filepath) as f:
        for line in f:
            item_id, _, title = line.strip().split(' ')
            mapper[item_id] = title.split(',')
    return mapper
