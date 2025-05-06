from tracardi.domain.profile import FlatProfile


def test_logger():
    fp = FlatProfile({
        "id": 1,
        "prop": {
            "a": 1
        }
    })

    assert fp['prop.a'] == 1
    assert fp.log.get_log() == {}

    fp['prop.a'] = 2
    assert 'prop.a' in fp.log.get_log().keys()
    assert fp['prop.a'] == 2

    # do not update change log
    fp['metadata.fields.xxx'] = 2
    assert 'metadata.fields.xxx' not in fp.log.get_log().keys()
