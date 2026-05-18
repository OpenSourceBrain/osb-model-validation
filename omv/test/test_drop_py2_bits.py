from contextlib import contextmanager
import types

from omv.engines import getnetpyne, getnrn


def test_install_neuron_defaults_to_modern_version(monkeypatch):
    pip_calls = []

    monkeypatch.setattr(getnrn, "pip_install", lambda spec: pip_calls.append(spec))
    monkeypatch.setattr(getnrn, "inform", lambda *args, **kwargs: None)
    monkeypatch.setitem(__import__("sys").modules, "neuron", types.SimpleNamespace())

    getnrn.install_neuron(None)

    assert pip_calls == [f"neuron=={getnrn.DEFAULT_NEURON_VERSION}"]


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
