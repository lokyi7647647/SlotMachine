betting_lines_options = [
  '1', '2', '3', 
  '1 2', '2 3', '1 3', '3 1', '2 1', '3 2',
  '1 2 3', '1 3 2', '3 2 1', '2 1 3',  '3 1 2', '2 3 1'
]
emoji_row = "[^ ]+ \| [^ ]+ \| [^ ]+\r\n"
deposit_prompt = "How much would you like to deposit\? \$"
balance_prompt = "Current balance is \$(\d+)\r\n"
start_game_prompt = "Press any key to start game \(ctrl d to quit\)"
bet_prompt = "Enter bet for each line\? \$"
lines_prompt = "Enter lines to bet on \(1-3\), separated by spaces \(eg\. 1 2\): "
total_bet_and_lines_confirmation = "You are betting \$(\d+) on the lines ((?:\d| )+)\r\n"
spin_output = f"{emoji_row}{emoji_row}{emoji_row}"
winning_output = (
  "You have won on lines: ([^\r\n]+)\r\n"
  "You won a total of \$(\d+)\r\n"
)
lost_output = "You lost \$(\d+)\r\n"
bal_gt_zero_output = "Current balance is \$(\d+)\r\n"
bal_eq_zero_output = "Your balance is \$0\r\n"
outputs = (
  rf"{deposit_prompt}\d+\r\n"
  rf"{balance_prompt}"
  rf"{start_game_prompt}\r\n"
  rf"{bet_prompt}\d+\r\n"
  rf"{lines_prompt}(\d| )+\r\n"
  rf"{total_bet_and_lines_confirmation}"
  rf"{spin_output}"
)
complete_round_win_output = (
  rf"{outputs}"
  rf"{winning_output}"
  rf"{lost_output}"
  rf"{bal_gt_zero_output}"
  rf"{start_game_prompt}(\^D\x08\x08)?"
)
complete_round_loss_output = (
  rf"{outputs}"
  rf"{lost_output}"
  rf"{bal_gt_zero_output}"
  rf"{start_game_prompt}(\^D\x08\x08)?"
)
complete_round_loss_output_when_bal_eq_zero = (
  rf"{outputs}"
  rf"{lost_output}"
  rf"{bal_eq_zero_output}"
  rf"{deposit_prompt}\d+\r\n"
  rf"{balance_prompt}"
  rf"{start_game_prompt}(\^D\x08\x08)?"
)