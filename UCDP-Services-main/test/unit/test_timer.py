from time import sleep

from tracardi.service.timer import Timer


def test_reset_timer_sets_time_to_zero():
    timer = Timer()
    assert timer.get_time('key1') == 0.0
    assert timer.get_time('key2') == 0.0

    timer.reset_timer('key1')
    assert timer.get_time('key1') != 0.0
    assert timer.get_time('key2') == 0.0

    sleep(0.1)

    assert timer.is_time_over('key1', 0.01)
    assert timer.is_time_over('key2', 10)

    timer.reset_timer('key2')
    assert not timer.is_time_over('key1', 1)
    assert not timer.is_time_over('key2', 1)