from io import StringIO
import pytest
from ...src.deposit import deposit


def test_deposit_valid(monkeypatch):
  monkeypatch.setattr("sys.stdin", StringIO('1'))
  assert deposit() == 1

def test_deposit_rejects_decimals(monkeypatch, capsys):
  monkeypatch.setattr("sys.stdin", StringIO('1.1'))
  with pytest.raises(EOFError):
    deposit()
  captured = capsys.readouterr()
  assert captured.err == "Deposit must be only digit (i.e 0-9)\n"

def test_deposit_rejects_zero(monkeypatch, capsys):
  monkeypatch.setattr("sys.stdin", StringIO('0'))
  with pytest.raises(EOFError):
    deposit()
  captured = capsys.readouterr()
  assert captured.err == "Deposit needs to be greater than 0.00\n"

def test_deposit_rejects_letters(monkeypatch, capsys):
  monkeypatch.setattr("sys.stdin", StringIO('hello world'))
  with pytest.raises(EOFError):
    deposit()
  captured = capsys.readouterr()
  assert captured.err == "Deposit must be only digit (i.e 0-9)\n"

def test_deposit_rejects_mix(monkeypatch, capsys):
  monkeypatch.setattr("sys.stdin", StringIO('1234a5'))
  with pytest.raises(EOFError):
    deposit()
  captured = capsys.readouterr()
  assert captured.err == "Deposit must be only digit (i.e 0-9)\n"