import subprocess


def test_invoke_from_command_line():
    output = subprocess.run(
        ["python", "-m", "audiomatch", "--help"], stdout=subprocess.PIPE,
    )
    assert "usage: audiomatch" in output.stdout.decode()
