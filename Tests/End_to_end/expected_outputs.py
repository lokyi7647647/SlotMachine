# Valid betting lines input
BETTING_LINE_OPTIONS = [
    '1', '2', '3', 
    '1 2', '2 3', '1 3', '3 1', '2 1', '3 2',
    '1 2 3', '1 3 2', '3 2 1', '2 1 3',  '3 1 2', '2 3 1'
]

# Basic Patterns
DEPOSIT_PROMPT_RE = r"How much would you like to deposit\? \$"
BALANCE_PROMPT_RE = r"Current balance is \$(\d+)\r\n"
START_GAME_PROMPT_RE = r"Press any key to start game \(ctrl d to quit\)"
BET_PROMPT_RE = r"Enter bet for each line\? \$"
LINES_PROMPT_RE = r"Enter lines to bet on \(1-3\), separated by spaces \(eg\. 1 2\): "
BETTING_INFO_CONFIRMATION_RE = r"You are betting \$(\d+) on the lines ((?:\d| )+)\r\n"
LINE_RE = r"[^ ]+ \| [^ ]+ \| [^ ]+\r\n"
CTRL_D_RE = r"\^D\x08\x08"

# Spin result patterns
SPIN_OUTCOME_RE = rf"{LINE_RE}{LINE_RE}{LINE_RE}"
WINNING_OUTCOME_RE = (
    r"You have won on lines: ([^\r\n]+)\r\n"
    r"You won a total of \$(\d+)\r\n"
)
LOST_OUTCOME_RE = r"You lost \$(\d+)\r\n"
BALANCE_IS_POSITIVE_RE = r"Current balance is \$(\d+)\r\n"
BALANCE_IS_ZERO_RE = r"Your balance is \$0\r\n"

# Combined patterns
DEPOSIT_START_PROMPT_RE = (
    rf"{DEPOSIT_PROMPT_RE}\d+\r\n"
    rf"{BALANCE_PROMPT_RE}"
    rf"{START_GAME_PROMPT_RE}"
)
PROMPTS_RE = (
    r"\r\n"
    rf"{BET_PROMPT_RE}\d+\r\n"
    rf"{LINES_PROMPT_RE}(\d| )+\r\n"
    rf"{BETTING_INFO_CONFIRMATION_RE}"
    rf"{SPIN_OUTCOME_RE}"
)
END_PROMPT_RE = (
    rf"{LOST_OUTCOME_RE}"
    rf"{BALANCE_IS_POSITIVE_RE}"
    rf"{START_GAME_PROMPT_RE}"
)
COMPLETE_ROUND_WIN_RE = (
    rf"{PROMPTS_RE}"
    rf"{WINNING_OUTCOME_RE}"
    rf"{END_PROMPT_RE}"
)
COMPLETE_ROUND_LOSS_RE = (
    rf"{PROMPTS_RE}"
    rf"{END_PROMPT_RE}"
)
COMPLETE_ROUND_LOSS_WITH_DEPOSIT_EQUAL_TOTAL_BET = (
    rf"{PROMPTS_RE}"
    rf"{LOST_OUTCOME_RE}"
    rf"{BALANCE_IS_ZERO_RE}"
    rf"{DEPOSIT_START_PROMPT_RE}"
)
RANDOM_ROUND_RE = (
    rf"({COMPLETE_ROUND_WIN_RE}|{COMPLETE_ROUND_LOSS_RE}|{COMPLETE_ROUND_LOSS_WITH_DEPOSIT_EQUAL_TOTAL_BET})"
    rf"{CTRL_D_RE}"
)