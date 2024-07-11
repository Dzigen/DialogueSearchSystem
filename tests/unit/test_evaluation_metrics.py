from fixtures import metrics_class

import pytest

@pytest.mark.parametrize("predicted_cands,actual_cands,k,actual_score", [
    ([1,2,3,4,5], [1,3,5], 1, 1),
    ([1,2,3,4,5], [1,3,5], 2, 0.5),
    ([1,2,3,4,5], [1,3,5], 3, 0.67),
    ([1,2,3,4,5], [1,3,5], 4, 0.5),
    ([1,2,3,4,5], [1,3,5], 5, 0.6),
    ([1,2,3,4,5], [1,2,3], 5, 0.6),
    ([1,2,3,4,5], [3,4,5], 5, 0.6)
])
def test_precision(metrics_class, predicted_cands, actual_cands, k, actual_score):
    assert abs(metrics_class.precision(predicted_cands, actual_cands, k) - actual_score) < 10e-3

@pytest.mark.parametrize("predicted_cands,actual_cands,k,actual_score", [
    ([1,2,3,4,5], [1,3,5], 1, 0.33),
    ([1,2,3,4,5], [1,3,5], 2, 0.33),
    ([1,2,3,4,5], [1,3,5], 3, 0.67),
    ([1,2,3,4,5], [1,3,5], 4, 0.67),
    ([1,2,3,4,5], [1,3,5], 5, 1),
])
def test_recall(metrics_class, predicted_cands, actual_cands, k, actual_score):
    assert abs(metrics_class.recall(predicted_cands, actual_cands, k) - actual_score) < 10e-3

@pytest.mark.parametrize("predicted_cands,actual_cands,k,actual_score", [
    ([1,2,3,4,5], [1,3,5], 1, 0.5),
    ([1,2,3,4,5], [1,3,5], 2, 0.4),
    ([1,2,3,4,5], [1,3,5], 3, 0.666),
    ([1,2,3,4,5], [1,3,5], 4, 0.571),
    ([1,2,3,4,5], [1,3,5], 5, 0.749),
])
def test_f1(metrics_class, predicted_cands, actual_cands, k, actual_score):
    assert abs(metrics_class.f1_score(predicted_cands, actual_cands, k) - actual_score) < 10e-3

@pytest.mark.parametrize("predicted_cands,actual_cands,actual_score", [
    ([[1,2,3,4,5]], [[1,3,5]], 0.7555)
])
def test_map(metrics_class, predicted_cands, actual_cands, actual_score):
    assert abs(metrics_class.mAP(predicted_cands, actual_cands) - actual_score) < 10e-3

@pytest.mark.parametrize("predicted_cands,actual_cands,actual_score", [
    ([[1,2,3,4,5]], [[1,3,5]], 1),
    ([[1,2,3,4,5]], [[2,5]], 0.5),
    ([[1,2,3,4,5]], [[5]], 0.2),
])
def test_mrr(metrics_class, predicted_cands, actual_cands, actual_score):
    assert abs(metrics_class.MRR(predicted_cands, actual_cands) - actual_score) < 10e-3