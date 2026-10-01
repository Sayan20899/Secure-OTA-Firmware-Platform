from ota.image import Version


def test_versions_are_orderable():
    assert Version.parse("1.1.0") > Version.parse("1.0.9")
    assert Version.parse("2.0.0") > Version.parse("1.9.9")


def test_version_string():
    assert str(Version.parse("v1.2.3")) == "1.2.3"
