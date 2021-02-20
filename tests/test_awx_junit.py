import pytest
import io
from awx_junit import awx_junit
import xml.etree.ElementTree as ET


@pytest.fixture
def awx_sample_output_single_entry():
    with open("tests/fixtures/awx_test_output_small.json", "r") as f:
        return io.StringIO(f.read())


@pytest.fixture
def awx_sample_output():
    with open("tests/fixtures/awx_test_output_full.json", "r") as f:
        return io.StringIO(f.read())


def test_generate_report(awx_sample_output_single_entry, capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest"])
    awx_junit.main(awx_sample_output_single_entry)
    captured = capsys.readouterr()
    tree = ET.fromstring(captured.out)
    assert tree.tag == "testsuites"


def test_xml_output_single_entry(awx_sample_output_single_entry, capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest"])
    awx_junit.main(awx_sample_output_single_entry)
    captured = capsys.readouterr()
    tree = ET.fromstring(captured.out)
    assert tree.tag == "testsuites"
    assert sum(1 for e in tree.iter("testsuite")) == 1
    assert tree[0].attrib["tests"] == "1"
    assert tree[0].attrib["name"] == "Do stuff task"
    assert tree[0].attrib["time"] == "1.10799"
    assert tree[0].attrib["failures"] == "0"
    assert tree[0].attrib["errors"] == "0"
    assert tree[0].attrib["skipped"] == "0"


def test_xml_output_multiple_entries(awx_sample_output, capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest"])
    awx_junit.main(awx_sample_output)
    captured = capsys.readouterr()
    tree = ET.fromstring(captured.out)
    assert tree.tag == "testsuites"
    assert sum(1 for e in tree.iter("testsuite")) == 4
    assert sum(1 for e in tree.iter("failure")) == 1
    assert sum(1 for e in tree.iter("skipped")) == 2
    assert tree.attrib["tests"] == "8"
    assert tree.attrib["failures"] == "1"
    assert tree.find("./testsuite[@name='Verify foo']").attrib["failures"] == "1"
    assert tree.find("./testsuite[@name='Check foobar task']").attrib["skipped"] == "2"
    assert tree.find("./testsuite[@name='Gathering Facts']").attrib["tests"] == "4"
    assert (
        tree.find("./testsuite[@name='Gathering Facts']").attrib["time"] == "7.417543"
    )


def test_pretty_print(awx_sample_output, capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest", "-p"])
    awx_junit.main(awx_sample_output)
    captured = capsys.readouterr()
    tree = ET.fromstring(captured.out)
    assert tree.tag == "testsuites"


def test_not_json(awx_sample_output, capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["pytest"])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        awx_junit.main(io.StringIO("foobar"))
    captured = capsys.readouterr()
    assert captured.err.startswith("Input is not a JSON")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
