import re
from .helper import is_input_digit
import sys

ROWS = 3

def is_lines_valid(list_of_lines):
  set_of_non_duplicates = set()
  for line in list_of_lines:
    if line in set_of_non_duplicates:
      print(f"Entered the line '{line}' more than once", file=sys.stderr)
      continue
    elif int(line) == 0:
      print(f"Line '0' is invalid. Lines need to be starting from '1'", file=sys.stderr)
      return False
    elif int(line) > ROWS:
      print(f"The line '{line}' entered exceeds the maximum available line, which is '{ROWS}'", file=sys.stderr)
      return False
    set_of_non_duplicates.add(line)
  return True

def is_total_bet_valid(balance, total_bet_amount):
  if balance < total_bet_amount:
    print(f"Your total bet amount of ${total_bet_amount} exceeds your current balance of ${balance}", file=sys.stderr)
    return False
  return True

def get_bet_lines(balance, bet_amount):
  while True:
    lines = input("Enter lines to bet on (1-3), separated by spaces (eg. 1 2): ")
    lines_without_space = re.sub(r" ", r"", lines)
    if not is_input_digit("Lines", lines_without_space, False):
      continue

    list_of_lines = re.findall(r"[0-9]+", lines)
    if not is_lines_valid(list_of_lines):
      continue

    # here we know its an int (whole number)
    num_lines = len(list_of_lines)
    total_bet_amount = num_lines * bet_amount
    if not is_total_bet_valid(balance, total_bet_amount):
      continue
    break 

  print(f"You are betting ${total_bet_amount} on the lines", *list_of_lines)
  return list_of_lines, balance - total_bet_amount, total_bet_amount