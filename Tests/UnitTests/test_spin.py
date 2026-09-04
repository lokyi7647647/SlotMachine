"""Test the output when a spin results in either a win or a loss"""

from ...src import spin as spin_module
from ...src.spin import spin
from ...src.bet_lines import get_bet_lines
import emoji
from io import StringIO

def test_spin_with_win(monkeypatch, capsys):
  # Mock stdin for reading the betting lines
  # by creating a file-like object and setting its content to the desired input
  # 1 2 -> each digit corresponds to a line on the slot machine
  monkeypatch.setattr("sys.stdin", StringIO('1 2'))
  balance = 10
  bet_amount = 5
  # net_balance = balance (10) - total_bet_amount (10)
  list_of_lines, net_balance, total_bet_amount = get_bet_lines(balance, bet_amount)
  assert net_balance == 0
  winnable_rows = lambda all_possible_emojis, k: [emoji.emojize(':thumbs_up:') for _ in range(k)]
  # Set random.sample to always give cols that form winnable rows/lines
  monkeypatch.setattr(spin_module.random, "sample", winnable_rows)
  # Each line win is $10 since symbol_value of thumbs_up ($2) * bet_amount ($5)
  # We have 2 line wins, so a total win amount of $20
  expected_new_balance = 20
  assert spin(list_of_lines, net_balance, bet_amount, total_bet_amount) == expected_new_balance
  captured = capsys.readouterr()
  assert captured.out == (
    "Enter lines to bet on (1-3), separated by spaces (eg. 1 2): "
    "You are betting $10 on the lines 1 2\n"
    "👍 | 👍 | 👍\n"
    "👍 | 👍 | 👍\n"
    "👍 | 👍 | 👍\n"
    "You have won on lines: 1 2\n"
    "You won a total of $20\n"
    "You lost $10\n"
  )

def col_generator_that_ensure_non_winneable_rows(all_possible_emojis, k, cols=[]):
  if len(cols) == 0:
    col = [emoji.emojize(":thumbs_up:"), emoji.emojize(":grinning_face:"), emoji.emojize(":star-struck:")]
  elif len(cols) == 1:
    col = [emoji.emojize(":thumbs_up:"), emoji.emojize(":grinning_face:"), emoji.emojize(":star-struck:")]
  elif len(cols) == 2:
    col = [emoji.emojize(":grinning_face:"), emoji.emojize(":thumbs_up:"), emoji.emojize(":thumbs_up:")]

  cols.append(col)
  return col


def test_spin_with_loss(monkeypatch, capsys):
  # Mock stdin for reading the betting lines
  # by creating a file-like object and setting its content to the desired input
  # 1 2 3 -> each digit is a line on the slot machine
  monkeypatch.setattr("sys.stdin", StringIO('1 2 3'))
  balance = 10
  bet_amount = 2
  # net_balance = balance (10) - total_bet_amount (6)
  list_of_lines, net_balance, total_bet_amount = get_bet_lines(balance, bet_amount)
  assert net_balance == 4
  # Set random.sample to never give cols that form winnable rows/lines
  monkeypatch.setattr(spin_module.random, "sample", col_generator_that_ensure_non_winneable_rows)
  # no wins so expect balance after spin be unchanged
  expected_new_balance = net_balance
  assert spin(list_of_lines, net_balance, bet_amount, total_bet_amount) == expected_new_balance
  captured = capsys.readouterr()
  assert captured.out == (
    "Enter lines to bet on (1-3), separated by spaces (eg. 1 2): "
    "You are betting $6 on the lines 1 2 3\n"
    "👍 | 👍 | 😀\n"
    "😀 | 😀 | 👍\n"
    "🤩 | 🤩 | 👍\n"
    "You lost $6\n"
  )