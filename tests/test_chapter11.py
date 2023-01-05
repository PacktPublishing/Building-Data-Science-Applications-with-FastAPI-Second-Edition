import pytest


def test_chapter11_load_digits():
    from chapter11.chapter11_load_digits import data, targets

    assert data[:, 0].size == targets.size


def test_chapter11_fit_predict():
    from chapter11.chapter11_fit_predict import accuracy

    assert accuracy == pytest.approx(0.83, rel=1e-2)


def test_chapter11_pipelines():
    from chapter11.chapter11_pipelines import accuracy

    assert accuracy == pytest.approx(0.83, rel=1e-2)


def test_chapter11_cross_validation():
    from chapter11.chapter11_cross_validation import score

    assert score.mean() == pytest.approx(0.80, rel=1e-2)
