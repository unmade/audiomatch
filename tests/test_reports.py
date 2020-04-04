from pathlib import Path

from audiomatch import reports


def test_console(capsys):
    matches = {
        (Path("sample-1/take-2.m4a"), Path("sample-1/take-1.m4a")): 0.77,
        (Path("sample-1/take-3.m4a"), Path("sample-1/take-1.m4a")): 0.75,
        (Path("sample-1/take-1.m4a"), Path("sample-2/take-4.m4a")): 0.00,
        (Path("sample-2/take-1.m4a"), Path("sample-1/take-1.m4a")): 0.00,
        (Path("sample-2/take-3.m4a"), Path("sample-1/take-1.m4a")): 0.00,
        (Path("sample-2/take-2.m4a"), Path("sample-1/take-1.m4a")): 0.00,
        (Path("sample-1/take-3.m4a"), Path("sample-1/take-2.m4a")): 0.78,
        (Path("sample-1/take-2.m4a"), Path("sample-2/take-4.m4a")): 0.00,
        (Path("sample-1/take-2.m4a"), Path("sample-2/take-1.m4a")): 0.00,
        (Path("sample-2/take-3.m4a"), Path("sample-1/take-2.m4a")): 0.00,
        (Path("sample-1/take-2.m4a"), Path("sample-2/take-2.m4a")): 0.00,
        (Path("sample-1/take-3.m4a"), Path("sample-2/take-4.m4a")): 0.00,
        (Path("sample-1/take-3.m4a"), Path("sample-2/take-1.m4a")): 0.00,
        (Path("sample-1/take-3.m4a"), Path("sample-2/take-3.m4a")): 0.00,
        (Path("sample-1/take-3.m4a"), Path("sample-2/take-2.m4a")): 0.00,
        (Path("sample-2/take-1.m4a"), Path("sample-2/take-4.m4a")): 0.62,
        (Path("sample-2/take-3.m4a"), Path("sample-2/take-4.m4a")): 0.60,
        (Path("sample-2/take-2.m4a"), Path("sample-2/take-4.m4a")): 0.60,
        (Path("sample-2/take-3.m4a"), Path("sample-2/take-1.m4a")): 0.64,
        (Path("sample-2/take-2.m4a"), Path("sample-2/take-1.m4a")): 0.66,
        (Path("sample-2/take-3.m4a"), Path("sample-2/take-2.m4a")): 0.62,
    }

    reports.console(matches)
    output = capsys.readouterr()
    assert output.out.splitlines() == [
        "sample-1/take-1.m4a",
        "sample-1/take-2.m4a",
        "sample-1/take-3.m4a",
        "---",
        "sample-2/take-1.m4a",
        "sample-2/take-2.m4a",
        "sample-2/take-3.m4a",
        "sample-2/take-4.m4a",
    ]


def test_console_for_transitive_matches(capsys):
    matches = {
        (Path("a"), Path("b")): 0.77,
        (Path("b"), Path("c")): 0.75,
    }

    reports.console(matches)
    output = capsys.readouterr()
    assert output.out.splitlines() == [
        "a",
        "b",
        "c",
    ]


def test_console_no_matches(capsys):
    matches = {
        (Path("take-3.m4a"), Path("take-1.m4a")): 0.00,
    }

    reports.console(matches)
    output = capsys.readouterr()
    assert output.out.splitlines() == [
        "No matches found.",
    ]
