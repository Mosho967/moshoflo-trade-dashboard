from ai.predictor import classify_trade


def test_low_volume_classification():
    assert classify_trade(50) == "LOW RISK"


def test_medium_volume_classification():
    assert classify_trade(5000) == "MEDIUM RISK"


def test_high_volume_classification():
    assert classify_trade(10000) == "HIGH RISK"
