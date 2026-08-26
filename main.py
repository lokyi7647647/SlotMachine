#!/usr/bin/env python3
import random
import emoji

COLS = 5
ROWS = 5

def is_input_digit(type, input):
  if not input.isdigit():
    print(f"{type} must be only digit (i.e 0-9)")
    return False
  input = int(input)
  if input <= 0:
    print(f"{type} needs to be greater than 0.00")
    return False
  return True
    
# def spin():
  

def get_bet():
  while True:
    bet_amount = input("How much do you want to bet for each line? $")
    if not is_input_digit("Bet", bet_amount):
      continue
    break
  return int(bet_amount)

def get_num_lines(amount, bet_amount):
  while True:
    num_lines = input("How many lines (i.e 1-5 lines) do you want to bet? ")
    if not is_input_digit("Number of lines", num_lines):
      continue
    # here we know its an int (whole number)
    num_lines = int(num_lines)
    bet_amount = num_lines * bet_amount
    if num_lines > ROWS:
      print(f"Number of lines to bet on exceeds the maximum of 5 lines")
      continue
    elif amount < bet_amount:
      print(f"Your total bet amount (${bet_amount}) exceeds your current balance (${amount})")
      continue 
    break 
  return num_lines


def deposit():
  while True:
    amount = input("How much would you like to deposit? $")
    if not is_input_digit("Deposit", amount):
      continue
    break
  amount = int(amount)
  return amount


    



def main():
  amount = deposit()
  while True:
    input("Press any key to start game (ctrl d to quit)")
    print(f"Current deposit is {amount}")
    bet = get_bet()
    num_lines = get_num_lines(amount, bet)
    # print(f"{bet}, {num_lines}")


    

try:
  main()
except EOFError:
  pass
  
