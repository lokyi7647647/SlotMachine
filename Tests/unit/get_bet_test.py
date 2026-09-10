"""
# tests / unit / get bet test

Test the get_bet function in reading valid/invalid bet amount per payline
"""

import pytest
from io import StringIO
from ...src.bet import get_bet


def test_bet_valid(monkeypatch):
    # Mock reading betting amount per line from stdin
    # by creating a file-like object and setting its content to the desired input
    monkeypatch.setattr("sys.stdin", StringIO('10'))
    assert get_bet(100) == 10

def test_bet_rejects_decimals(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO('2.0'))
    with pytest.raises(EOFError):
        get_bet(100)
    captured = capsys.readouterr()
    assert captured.err == "Bet must be only digit (i.e 0-9)\n"

def test_bet_rejects_zero(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO('0'))
    with pytest.raises(EOFError):
        get_bet(100)
    captured = capsys.readouterr()
    assert captured.err == "Bet needs to be greater than 0.00\n"

def test_bet_rejects_bigger_than_balance(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO('11'))
    with pytest.raises(EOFError):
        get_bet(10)
    captured = capsys.readouterr()
    assert captured.err == "Your bet amount of $11 exceeds your balance of $10\n"

def test_bet_rejects_mix(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO('a123'))
    with pytest.raises(EOFError):
        get_bet(100)
    captured = capsys.readouterr()
    assert captured.err == "Bet must be only digit (i.e 0-9)\n"

def test_bet_equals_balance(monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO('100'))
    assert get_bet(100) == 100