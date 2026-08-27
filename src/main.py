#!/usr/bin/env python3
from deposit import deposit
from bet import get_bet
from bet_lines import get_num_lines
from spin import spin

def main():
  balance = deposit()
  while True:
    print(f"Current balance is {balance}")
    input("Press any key to start game (ctrl d to quit)")
    bet_amount = get_bet(balance)
    list_of_lines, balance, total_bet_amount = get_num_lines(balance, bet_amount)
    balance = spin(list_of_lines, balance, bet_amount, total_bet_amount)
    if balance == 0:
      print(f"Your balance is $0")
      balance = deposit()


try:
  main()
except EOFError:
  pass
  
