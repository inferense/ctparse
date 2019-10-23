"""This module cointains the implementation of the scorer based on naive bayes."""
import bz2
import math
import pickle
from datetime import datetime
from typing import Sequence, Tuple, Union

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.base import BaseEstimator

from .scorer import Scorer
from .partial_parse import PartialParse
from .types import Time, Interval


class NaiveBayesScorer(Scorer):

    def __init__(self, nb_model: BaseEstimator) -> None:
        """Scorer based on a naive bayes estimator. 

        This scorer models the probability of having a correct parse, conditioned
        on the sequence of rules (expressed as a categorical feature) that led to
        that parse.

        The score is also modified by a "length" factor that penalizes parses that
        cover a smaller part of the text string.

        :param nb_model:
            A scikit-learn style Estimator that was trained on a corpus that takes
            a Sequence[Sequence[str]] as X (each entry is a sequence of rule identifiers)
            and a Sequence[int] in the set {-1, 1} that indicates if the parse
            was correct or incorrect.
        """
        self._model = nb_model

    @classmethod
    def from_model_file(cls, fname: str) -> 'NaiveBayesScorer':
        with bz2.open(fname, 'rb') as fd:
            return cls(pickle.load(fd))

    def score(self, txt: str, ts: datetime, partial_parse: PartialParse) -> float:
        # Penalty for partial matches
        max_covered_chars = partial_parse.prod[-1].mend - partial_parse.prod[0].mstart
        len_score = math.log(max_covered_chars/len(txt))

        X = _feature_extractor(txt, ts, partial_parse)
        pred = self._model.predict_log_proba([X])

        # NOTE: the prediction is log-odds, or logit
        model_score = float(pred[:, 1] - pred[:, 0])

        return model_score + len_score

    def score_final(self, txt: str, ts: datetime,
                    partial_parse: PartialParse, prod: Union[Time, Interval]) -> float:
        # The difference between the original score and final score is that in the
        # final score, the len_score is calculated based on the length of the final
        # production
        len_score = math.log(len(prod)/len(txt))

        X = _feature_extractor(txt, ts, partial_parse)
        pred = self._model.predict_log_proba([X])

        # NOTE: the prediction is log-odds, or logit
        model_score = float(pred[:, 1] - pred[:, 0])

        return model_score + len_score


def _feature_extractor(txt: str, ts: datetime, partial_parse: PartialParse) -> Sequence[str]:
    return [str(r) for r in partial_parse.rules]


def _identity(x):
    return x


def train_naive_bayes(X: Sequence[Sequence[str]], y: Sequence[int], output_fname: str) -> None:
    """Train a naive bayes model for NaiveBayesScorer"""
    # Create and train the pipeline
    model = make_pipeline(
        CountVectorizer(ngram_range=(1, 3), lowercase=False,
                        tokenizer=_identity),
        MultinomialNB(alpha=1.0))
    model.fit(X, y)

    # Make sure that class order is -1, 1
    assert model.classes_[0] == -1

    # Save the model to disk
    with bz2.open(output_fname, 'wb') as fd:
        pickle.dump(model, fd)
