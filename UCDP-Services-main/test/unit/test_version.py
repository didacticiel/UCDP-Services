from tracardi.domain.version import Version


def test_version_name():
    version = Version(version="1.0.x", db_version="090x")
    assert version.name == Version._generate_name("090x")
