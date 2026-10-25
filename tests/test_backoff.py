import pytest

from core.backoff import ExponentialBackoff


def test_backoff_doubles_delay():
    backoff = ExponentialBackoff(base_delay=1, max_delay=30)

    assert backoff.next_delay() == 1
    assert backoff.next_delay() == 2
    assert backoff.next_delay() == 4
    assert backoff.next_delay() == 8


def test_backoff_respects_max_delay():
    backoff = ExponentialBackoff(base_delay=1, max_delay=5)

    assert backoff.next_delay() == 1
    assert backoff.next_delay() == 2
    assert backoff.next_delay() == 4
    assert backoff.next_delay() == 5
    assert backoff.next_delay() == 5


def test_backoff_reset():
    backoff = ExponentialBackoff(base_delay=1, max_delay=30)

    backoff.next_delay()
    backoff.next_delay()
    backoff.reset()

    assert backoff.next_delay() == 1


def test_backoff_rejects_invalid_base_delay():
    with pytest.raises(ValueError):
        ExponentialBackoff(base_delay=0, max_delay=30)


def test_backoff_rejects_max_delay_below_base_delay():
    with pytest.raises(ValueError):
        ExponentialBackoff(base_delay=5, max_delay=2)
