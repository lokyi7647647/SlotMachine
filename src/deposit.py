from .helper import is_input_digit

def deposit():
  while True:
    amount = input("How much would you like to deposit? $")
    if not is_input_digit("Deposit", amount):
      continue
    break
  amount = int(amount)
  return amount
