import pytest

import datasets_preparation.utils.retry as retry_module


def test_prepare_with_retries_retries_broken_pipe(monkeypatch):
    calls = 0

    def f():
        nonlocal calls
        calls += 1

        if calls == 1:
            raise BrokenPipeError('broken pipe')

    monkeypatch.setattr(
        retry_module.time,
        'sleep',
        lambda _: None
    )

    retry_module.prepare_with_retries(
        f=f,
        max_retries=1
    )

    assert calls == 2

def test_prepare_with_retries_does_not_retry_non_retryable_error():
    calls = 0

    def f():
        nonlocal calls
        calls += 1
        raise ValueError('bad config')

    with pytest.raises(ValueError, match='bad config'):
        retry_module.prepare_with_retries(
            f=f,
            max_retries=10
        )

    assert calls == 1

def test_retryable_preparation_error_checks_exception_chain():
    try:
        try:
            raise BrokenPipeError('broken pipe')
        except BrokenPipeError as e:
            raise RuntimeError('wrapped') from e
    except RuntimeError as e:
        assert retry_module.is_retryable_preparation_error(e)

def test_prepare_with_retries_stops_after_max_retries(monkeypatch):
    calls = 0

    def f():
        nonlocal calls
        calls += 1
        raise BrokenPipeError('broken pipe')

    monkeypatch.setattr(
        retry_module.time,
        'sleep',
        lambda _: None
    )

    with pytest.raises(BrokenPipeError):
        retry_module.prepare_with_retries(
            f=f,
            max_retries=2
        )

    assert calls == 3
