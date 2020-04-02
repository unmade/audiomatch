from pathlib import Path
from unittest import mock

import pytest

from audiomatch import cli


@pytest.mark.parametrize(
    ["cli_args", "call_args"],
    [
        (
            ["audiomatch", "directory"],
            mock.call(Path("directory"), length=120, extensions=None),
        ),
        (
            ["audiomatch", "directory", "--length", "60"],
            mock.call(Path("directory"), length=60, extensions=None),
        ),
        (
            ["audiomatch", "directory", "-e", ".mp3"],
            mock.call(Path("directory"), length=120, extensions=[".mp3"]),
        ),
        (
            ["audiomatch", "directory", "-e", ".mp3", "-e", ".m4a"],
            mock.call(Path("directory"), length=120, extensions=[".mp3", ".m4a"]),
        ),
    ],
)
def test_cli(cli_args, call_args):
    with mock.patch("sys.argv", cli_args):
        with mock.patch("audiomatch.match.match") as mocked_match:
            cli.invoke()
    assert mocked_match.call_args == call_args
