import pytest

from io import StringIO
from ...src.bet_lines import get_bet_lines

@pytest.fixture
def balance_and_bet():
  return 10, 2

def test_get_bet_valid(monkeypatch, capsys, balance_and_bet):
  # mocking stdin to allow get_bet_lines() to read input
  # 1 2 3 -> each digit is a line on the slot machine
  monkeypatch.setattr("sys.stdin", StringIO('1 2 3'))
  balance, bet_amount = balance_and_bet
  get_bet_lines(balance, bet_amount)
  captured = capsys.readouterr()
  assert captured.out == "Enter lines to bet on (1-3), separated by spaces (eg. 1 2): You are betting $6 on the lines 1 2 3\n"

def test_get_bet_invalid_zeroth_line(monkeypatch, capsys, balance_and_bet):
  # slot machine can only have line 1 to 3, line 0 is in valid
  monkeypatch.setattr("sys.stdin", StringIO('0'))
  balance, bet_amount = balance_and_bet
  with pytest.raises(EOFError):
    get_bet_lines(balance, bet_amount)
  captured = capsys.readouterr()
  assert captured.err == "Line 0 is invalid. Lines need to be starting from 1\n"

def test_lines_contain_bigger_than_3(monkeypatch, capsys, balance_and_bet):
  # slot machine can only have line 1 to 3, line 4 is in valid
  monkeypatch.setattr("sys.stdin", StringIO('1 4 3'))
  balance, bet_amount = balance_and_bet
  with pytest.raises(EOFError):
    get_bet_lines(balance, bet_amount)
  captured = capsys.readouterr()
  assert captured.err == "The line 4 entered exceeds the capacity of at most line 3\n"

def test_lines_contain_non_digits(monkeypatch, capsys, balance_and_bet):
  monkeypatch.setattr("sys.stdin", StringIO('1a 2'))
  balance, bet_amount = balance_and_bet
  with pytest.raises(EOFError):
    get_bet_lines(balance, bet_amount)
  captured = capsys.readouterr()
  assert captured.err == "Lines must be only digit (i.e 0-9)\n"

def test_lines_contain_one_duplicates(monkeypatch, capsys, balance_and_bet):
  monkeypatch.setattr("sys.stdin", StringIO('1 1 2'))
  balance, bet_amount = balance_and_bet
  get_bet_lines(balance, bet_amount)
  captured = capsys.readouterr()
  assert captured.err == "Entered the line 1 more than once\n"

def test_lines_contain_two_duplicates(monkeypatch, capsys, balance_and_bet):
  monkeypatch.setattr("sys.stdin", StringIO('1 1 2 2'))
  balance, bet_amount = balance_and_bet
  get_bet_lines(balance, bet_amount)
  captured = capsys.readouterr()
  assert captured.err == (
    "Entered the line 1 more than once\n"
    "Entered the line 2 more than once\n"
  )

def test_total_bet_exceeds_balance(monkeypatch, capsys):
  monkeypatch.setattr("sys.stdin", StringIO('1 2'))
  balance = 10
  bet_amount = 6
  with pytest.raises(EOFError):
    get_bet_lines(balance, bet_amount)
  captured = capsys.readouterr()
  # two lines (i.e 1 2), each cost $6, so a total bet is $12
  assert captured.err == "Your total bet amount of $12 exceeds your current balance of $10\n"

def test_total_bet_equals_balance(monkeypatch, capsys):
  monkeypatch.setattr("sys.stdin", StringIO('1 2'))
  balance = 10
  bet_amount = 5
  get_bet_lines(balance, bet_amount)
  captured = capsys.readouterr()
  # two lines (i.e 1 2), each cost $6, so a total bet is $10
  assert captured.out == "Enter lines to bet on (1-3), separated by spaces (eg. 1 2): You are betting $10 on the lines 1 2\n"