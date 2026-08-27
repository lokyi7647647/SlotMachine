import random
import emoji

ROWS = 3
COLS = 3

symbol_count = {
  "thumbs_up": 2,
  "grinning_face" : 1,
  "star-struck" : 1,
  "smiling_face_with_open_hands": 1
}

symbol_value = {
  ":thumbs_up:": 2,
  ":grinning_face:" : 4,
  ":star-struck:" : 5,
  ":smiling_face_with_open_hands:": 5
}

def print_spin(matrix):
  for ith_component in range(ROWS):
      for ith_column, column in enumerate(matrix):
        if ith_column != len(matrix) - 1:
          print(f"{column[ith_component]}", end=' | ')
        else:
          print(f"{column[ith_component]}")

def spin(list_of_lines, balance, bet_amount, total_bet_amount):
  all_possible_emojis = [emoji.emojize(f":{symbol}:") for symbol, freq in symbol_count.items() for _ in range(freq)]
  matrix = [random.sample(all_possible_emojis, k=ROWS) for _ in range(COLS)]
  
  # determine if there is a win
  global winning_lines
  winning_lines = []
  winnings = 0
  # print(list_of_lines)
  for line in list_of_lines:
    line = int(line) - 1
    # Fetch the line's starting symbol which is at the first tranpose column
    expected_symbol = matrix[0][line]
    # Checks whether all the transpose columns contain the same symbol at the ith component
    # which builds the line when undoing the tranpose of this 'matrix'
    for tranpose_column in matrix:
      if expected_symbol != tranpose_column[line]:
        break
    else:
      winning_lines.append(line + 1)
      winnings += symbol_value[emoji.demojize(expected_symbol)] * bet_amount

  print_spin(matrix)
  if winning_lines != []:
    print("You have won on lines:", *winning_lines)
    print(f"You won a total of ${winnings}")
  print(f"You lost ${total_bet_amount}")

  balance += winnings
  return balance