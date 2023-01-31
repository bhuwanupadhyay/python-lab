#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from typing import Iterator, Tuple

import dedupe
from dedupe._typing import (
    Literal,
    RecordDictPair,
    TrainingData,
)
from dedupe.core import unique

IndicesIterator = Iterator[Tuple[int, int]]


def _print(*args) -> None:
    print(*args, file=sys.stderr)


LabeledPair = Tuple[RecordDictPair, Literal["match", "distinct", "unsure"]]


def _mark_pair(deduper: dedupe.api.ActiveMatching, labeled_pair: LabeledPair) -> None:
    record_pair, label = labeled_pair
    examples: TrainingData = {"distinct": [], "match": []}
    if label == "unsure":
        # See https://github.com/dedupeio/dedupe/issues/984 for reasoning
        examples["match"].append(record_pair)
        examples["distinct"].append(record_pair)
    else:
        # label is either "match" or "distinct"
        examples[label].append(record_pair)
    deduper.mark_pairs(examples)


def console_label(deduper: dedupe.api.ActiveMatching, positive=5, negative=5) -> None:
    finished = False
    use_previous = False
    fields = unique(var.field for var in deduper.data_model.primary_variables)

    buffer_len = 1  # Max number of previous operations
    unlabeled: list[RecordDictPair] = []
    labeled: list[LabeledPair] = []

    n_match = len(deduper.training_pairs["match"])
    n_distinct = len(deduper.training_pairs["distinct"])

    while not finished:
        if use_previous:
            record_pair, label = labeled.pop(0)
            if label == "match":
                n_match -= 1
            elif label == "distinct":
                n_distinct -= 1
            use_previous = False
        else:
            try:
                if not unlabeled:
                    unlabeled = deduper.uncertain_pairs()

                record_pair = unlabeled.pop()
            except IndexError:
                break

        for record in record_pair:
            for field in fields:
                line = "%s : %s" % (field, record[field])
                _print(line)
            _print()
        _print(f"{n_match}/10 positive, {n_distinct}/10 negative")
        if positive > 0:
            user_input = 'y'
            positive = positive - 1
        elif negative > 0:
            user_input = 'n'
            negative = negative - 1
        else:
            user_input = 'f'

        _print(f"Do these records refer to the same thing? -> {user_input}")

        if user_input == "y":
            labeled.insert(0, (record_pair, "match"))
            n_match += 1
        elif user_input == "n":
            labeled.insert(0, (record_pair, "distinct"))
            n_distinct += 1
        elif user_input == "u":
            labeled.insert(0, (record_pair, "unsure"))
        elif user_input == "f":
            _print("Finished labeling")
            finished = True
        elif user_input == "p":
            use_previous = True
            unlabeled.append(record_pair)

        while len(labeled) > buffer_len:
            _mark_pair(deduper, labeled.pop())

    for labeled_pair in labeled:
        _mark_pair(deduper, labeled_pair)
