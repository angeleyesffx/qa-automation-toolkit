import runpy
import sys
import importlib
import pytest
from qaforge.cli import main


def test_main_returns_zero():
    assert main([]) == 0


def test_main_module_runs_via_runpy(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["qaforge"])
    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("qaforge", run_name="__main__")
    assert exc_info.value.code == 0


def test_init_fallback_version_when_version_module_missing(monkeypatch):
    import qaforge
    original = sys.modules.get('qaforge._version')

    monkeypatch.setitem(sys.modules, 'qaforge._version', None)
    importlib.reload(qaforge)
    version = qaforge.__version__

    monkeypatch.setitem(sys.modules, 'qaforge._version', original)
    importlib.reload(qaforge)

    assert version == "0.0.4"
