# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import math
import unittest
import sumy.summarizers.lex_rank as lex_rank_module

from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers.czech import stem_word
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words
from ..utils import build_document, load_resource


class TestLexRank(unittest.TestCase):
    def test_numpy_not_installed(self):
        summarizer = LexRankSummarizer()

        numpy = lex_rank_module.numpy
        lex_rank_module.numpy = None

        self.assertRaises(ValueError, summarizer, build_document(), 10)

        lex_rank_module.numpy = numpy

    def test_tf_metrics(self):
        summarizer = LexRankSummarizer()

        sentences = [
            ("this", "sentence", "is", "simple", "sentence"),
            ("this", "is", "simple", "sentence", "yes", "is", "too", "too", "too"),
        ]
        metrics = summarizer._compute_tf(sentences)

        expected = [
            {"this": 1/2, "is": 1/2, "simple": 1/2, "sentence": 1.0},
            {"this": 1/3, "is": 2/3, "yes": 1/3, "simple": 1/3, "sentence": 1/3, "too": 1.0},
        ]
        self.assertEqual(expected, metrics)

    def test_idf_metrics(self):
        summarizer = LexRankSummarizer()

        sentences = [
            ("this", "sentence", "is", "simple", "sentence",),
            ("this", "is", "simple", "sentence", "yes", "is", "too", "too", "too",),
            ("not", "every", "sentence", "makes", "me", "happy",),
            ("yes",),
            (),
            ("every", "day", "is", "happy", "day",),
        ]
        metrics = summarizer._compute_idf(sentences)

        expected = {
            "this": 6/2,
            "is": 6/3,
            "yes": 6/2,
            "simple": 6/2,
            "sentence": 6/3,
            "too": 6/1,
            "not": 6/1,
            "every": 6/2,
            "makes": 6/1,
            "me": 6/1,
            "happy": 6/2,
            "day": 6/1,
        }
        self.assertEqual(expected, metrics)

    def test_modified_cosine_computation(self):
        summarizer = LexRankSummarizer()

        sentence1 = ["this", "sentence", "is", "simple", "sentence"]
        tf1 = {"this": 1/2, "sentence": 1.0, "is": 1/2, "simple": 1/2}
        sentence2 = ["this", "is", "simple", "sentence", "yes", "is", "too", "too"]
        tf2 = {"this": 1/2, "is": 1.0, "simple": 1/2, "sentence": 1/2, "yes": 1/2, "too": 1.0}
        idf = {
            "this": 2/2,
            "sentence": 2/2,
            "is": 2/2,
            "simple": 2/2,
            "yes": 2/1,
            "too": 2/1,
        }

        numerator = sum(tf1[t]*tf2[t]*idf[t]**2 for t in ["this", "sentence", "is", "simple"])
        denominator1 = math.sqrt(sum((tf1[t]*idf[t])**2 for t in sentence1))
        denominator2 = math.sqrt(sum((tf2[t]*idf[t])**2 for t in sentence2))

        expected = numerator / (denominator1 * denominator2)
        cosine = summarizer._compute_cosine(sentence1, sentence2, tf1, tf2, idf)
        self.assertEqual(expected, cosine)

    def test_article_example(self):
        """Source: http://www.prevko.cz/dite/skutecne-pribehy-deti"""
        parser = PlaintextParser.from_string(
            load_resource("articles/prevko_cz_1.txt"),
            Tokenizer("czech")
        )
        summarizer = LexRankSummarizer(stem_word)
        summarizer.stop_words = get_stop_words("czech")

        sentences = summarizer(parser.document, 20)
        self.assertEqual(len(sentences), 20)
