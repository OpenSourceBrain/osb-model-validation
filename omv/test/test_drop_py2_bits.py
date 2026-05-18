from contextlib import contextmanager
import sys
import types

import pytest

from omv.engines import getnetpyne, getnrn


def test_install_neuron_defaults_to_modern_version(monkeypatch):
    pip_calls = []

    monkeypatch.setattr(getnrn, "pip_install", lambda spec: pip_calls.append(spec))
    monkeypatch.setattr(getnrn, "inform", lambda *args, **kwargs: None)
    monkeypatch.setitem(sys.modules, "neuron", types.SimpleNamespace())

    getnrn.install_neuron(None)

    assert pip_calls == [f"neuron=={getnrn.DEFAULT_NEURON_VERSION}"]


@pytest.mark.parametrize("version", ["7.8.1", "8.2.7"])
def test_install_neuron_supported_versions_use_pip(monkeypatch, version):
    pip_calls = []

    monkeypatch.setattr(getnrn, "pip_install", lambda spec: pip_calls.append(spec))
    monkeypatch.setattr(getnrn, "inform", lambda *args, **kwargs: None)
    monkeypatch.setitem(sys.modules, "neuron", types.SimpleNamespace())

    getnrn.install_neuron(version)

    assert pip_calls == [f"neuron=={version}"]


@pytest.mark.parametrize(
    "version,expected",
    [("7.8", True), ("7.8.1", True), ("8.2.7", True), ("7.80", False), ("7.7.2", False)],
)
def test_supports_pip_install_matches_supported_families(version, expected):
    assert getnrn._supports_pip_install(version) is expected


def test_install_netpyne_without_version_only_installs_package(monkeypatch):
    pip_calls = []

    @contextmanager
    def no_op_working_dir(_):
        yield

    monkeypatch.setattr(getnetpyne.os.path, "isdir", lambda _: True)
    monkeypatch.setattr(getnetpyne, "working_dir", no_op_working_dir)
    monkeypatch.setattr(getnetpyne, "check_output", lambda *_: "")
    monkeypatch.setattr(getnetpyne, "pip_install", lambda spec: pip_calls.append(spec))

    getnetpyne.install_netpyne()

    assert pip_calls == ["."]
