import pytest
import random
import builtins
import sys
import pathlib

# Patch sys.path so we can import the module directly from py/
import importlib.util

MODULE_PATH = str(pathlib.Path(__file__).parent.parent.parent / "py" / "generate_compose.py")
spec = importlib.util.spec_from_file_location("generate_compose", MODULE_PATH)
generate_compose = importlib.util.module_from_spec(spec)
sys.modules["generate_compose"] = generate_compose
spec.loader.exec_module(generate_compose)

def test_generate_names_basic():
    assert generate_compose.generate_names(3, "node") == ["node_1", "node_2", "node_3"]
    assert generate_compose.generate_names(0, "n") == []
    assert generate_compose.generate_names(1, "bitcoin") == ["bitcoin_1"]

def test_compute_ports_basic():
    ports = generate_compose.compute_ports(2, 1000, 2000, "n")
    assert ports == {"n_1": (1000, 2000), "n_2": (1002, 2002)}
    ports = generate_compose.compute_ports(0, 100, 200, "x")
    assert ports == {}

def test_generate_peers_deterministic(monkeypatch):
    # Patch random to make the test deterministic
    monkeypatch.setattr(random, "randint", lambda a, b: 1)
    monkeypatch.setattr(random, "sample", lambda le, n: le[:n])
    names = ["n1", "n2", "n3"]
    peers = generate_compose.generate_peers(names, 2)
    for k, v in peers.items():
        assert len(v) == 1
        assert k not in v
        assert set(v).issubset(set(names) - {k})

def test_generate_peers_max_peers(monkeypatch):
    # If max_peers > available, should not exceed available
    monkeypatch.setattr(random, "randint", lambda a, b: b)
    monkeypatch.setattr(random, "sample", lambda le, n: le[:n])
    names = ["a", "b", "c", "d"]
    peers = generate_compose.generate_peers(names, 10)
    for _, v in peers.items():
        assert len(v) == len(names) - 1

def test_generate_command_addnode_and_logging(tmp_path, monkeypatch):
    # Prepare a fake template file
    template = (
        "user={RPCUSER}\n"
        "pass={RPCPASSWORD}\n"
        "max={MAXCONNECTIONS}\n"
        "rpc={RPCPORT}\n"
        "p2p={P2PPORT}\n"
        "{ADDNODE}\n"
    )
    template_path = tmp_path / "cmd.template"
    template_path.write_text(template)

    # Patch logging flags
    monkeypatch.setattr(generate_compose, "LOG_NET_ENABLED", True)
    monkeypatch.setattr(generate_compose, "LOG_MEMPOOL_ENABLED", True)

    all_ports = {"n2": (1002, 2002), "n3": (1004, 2004)}
    peers = ["n2", "n3"]
    result = generate_compose.generate_command(
        str(template_path),
        rpc_user="alice",
        rpc_password="pw",
        max_peers=5,
        rpc_port=1000,
        p2p_port=2000,
        peers=peers,
        all_ports=all_ports,
    )
    assert "user=alice" in result
    assert "-addnode=n2:2002" in result
    assert "-addnode=n3:2004" in result
    assert "-debug=net" in result
    assert "-debug=mempool" in result

def test_generate_command_template_extension(tmp_path):
    # Should raise if not .template
    with pytest.raises(ValueError):
        generate_compose.generate_command(
            "notemplate.txt", "u", "p", 1, 2, 3, [], {}
        )

def test_generate_command_no_logging(tmp_path, monkeypatch):
    template_path = tmp_path / "cmd.template"
    template_path.write_text("{ADDNODE}")
    monkeypatch.setattr(generate_compose, "LOG_NET_ENABLED", False)
    monkeypatch.setattr(generate_compose, "LOG_MEMPOOL_ENABLED", False)
    all_ports = {"n2": (1002, 2002)}
    peers = ["n2"]
    result = generate_compose.generate_command(
        str(template_path),
        rpc_user="a",
        rpc_password="b",
        max_peers=1,
        rpc_port=1,
        p2p_port=2,
        peers=peers,
        all_ports=all_ports,
    )
    assert "-addnode=n2:2002" in result
    assert "-debug" not in result

def test_export_data_creates_files(tmp_path, monkeypatch):
    # Patch print to suppress output
    monkeypatch.chdir(tmp_path)
    all_ports = {"n1": (1001, 2001), "n2": (1003, 2003)}
    node_names = ["n1", "n2"]
    names_path = tmp_path / "docker" / "data" / ".env.node_names"
    ports_path = tmp_path / "docker" / "data" / ".env.rpc_ports"
    generate_compose.export_data(all_ports, node_names, output_dir="data")
    assert names_path.exists()
    assert ports_path.exists()
    names_content = names_path.read_text()
    ports_content = ports_path.read_text()
    assert "n1" in names_content and "n2" in names_content
    assert "N1_RPC_PORT=1001" in ports_content
    assert "N2_RPC_PORT=1003" in ports_content

def test_export_data_prints(monkeypatch, tmp_path):
    # Patch print to capture output
    monkeypatch.chdir(tmp_path)
    printed = []
    monkeypatch.setattr(builtins, "print", lambda *a, **k: printed.append(a[0]))
    all_ports = {"n1": (1, 2)}
    node_names = ["n1"]
    generate_compose.export_data(all_ports, node_names, output_dir="data")
    assert any("Node names exported" in s for s in printed)
    assert any("RPC ports exported" in s for s in printed)