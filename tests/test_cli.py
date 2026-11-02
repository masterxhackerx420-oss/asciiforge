import io
import sys

from asciiforge.cli import main


def run(capsys, *args):
    code = main(list(args))
    out = capsys.readouterr()
    return code, out.out, out.err


def test_renders_multiple_lines(capsys):
    code, out, _ = run(capsys, "hello", "--width", "200")
    assert code == 0 and len(out.strip().splitlines()) >= 3


def test_list_includes_known_fonts(capsys):
    _, out, _ = run(capsys, "--list")
    for f in ("standard", "slant", "doom"):
        assert f in out.split()


def test_unknown_font_clean_error(capsys):
    code, out, err = run(capsys, "hi", "-f", "nope-not-a-font")
    assert code != 0 and "unknown font" in err and "Traceback" not in err


def test_stdin_input(capsys, monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("piped\n"))
    code, out, _ = run(capsys, "--width", "200")
    assert code == 0 and out.strip()


def test_border_wraps_output(capsys):
    _, out, _ = run(capsys, "hi", "--border", "--width", "200")
    lines = out.rstrip("\n").splitlines()
    assert lines[0].startswith("+-") and lines[-1].startswith("+-")
    assert all(l.startswith("|") and l.endswith("|") for l in lines[1:-1])


def test_wrapping_respects_width(capsys):
    _, out, _ = run(capsys, "the quick brown fox jumps", "--width", "40")
    assert max(len(l) for l in out.splitlines()) <= 40
    _, wide, _ = run(capsys, "the quick brown fox jumps", "--width", "500")
    assert len(out.splitlines()) > len(wide.splitlines())


def test_output_file(capsys, tmp_path):
    f = tmp_path / "art.txt"
    run(capsys, "ok", "-o", str(f))
    assert f.read_text().strip()
