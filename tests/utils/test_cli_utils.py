from aspen.utils.cli_utils import strtobool


def test_strtobool():
    for s in ["TRUE", "true", "T", "yes", "1"]:
        assert strtobool(s) is True

    for s in ["FALSE", "false", "F", "no", "0"]:
        assert strtobool(s) is False
