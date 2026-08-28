from .helper import is_input_digit
import sys

def get_bet(balance):
  while True:
    bet_amount = input("Enter bet for each line? $")
    if not is_input_digit("Bet", bet_amount):
      continue
    # what if bet amount is greater then balance
    bet_amount = int(bet_amount)
    if bet_amount > balance:
      print(f"Your bet amount of ${bet_amount} exceeds your balance of ${balance}", file=sys.stderr)
      continue
    break
  
  return bet_amount