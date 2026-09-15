"""
# tests / end to end / slotmachine helpers

Provide helper functions that assist testing the Slotmachine command line interface
"""

import random
import re

import pexpect
import emoji
import pytest

from ...src.spin import symbol_value
from .expected_outputs import (
    BETTING_LINE_OPTIONS,
    DEPOSIT_PROMPT_RE,
    BALANCE_PROMPT_RE,
    START_GAME_PROMPT_RE,
    BET_PROMPT_RE,
    LINES_PROMPT_RE,
    BETTING_INFO_CONFIRMATION_RE,
    SPIN_OUTCOME_RE,
    WINNING_OUTCOME_RE,
    LOST_OUTCOME_RE,
    BALANCE_IS_POSITIVE_RE,
    BALANCE_IS_ZERO_RE
)


# Generate random valid inputs for a round
def user_input_generator(bal_equal_total_bet, balance=None):
    if balance == None:
        bet_amount = random.randint(1, 100)
        betting_lines = random.choice(BETTING_LINE_OPTIONS)
        num_of_betting_lines = len(betting_lines.split())
        total_bet = bet_amount * num_of_betting_lines
        if bal_equal_total_bet:
            balance = total_bet
        else:
            balance = random.choice(
                [
                    n 
                    for n in range(bet_amount + 1, bet_amount * 5) 
                    if n > total_bet
                ]
            )
    else:
        # Generate the next rounds' input following the previous round
        bet_amount = random.randint(1, balance)

        # Ensure valid betting line, where total bet doesn't 
        # exceed the current balance
        betting_lines = random.choice(
            [
                n 
                for n in BETTING_LINE_OPTIONS 
                if (len(n.split()) * bet_amount <= balance)
            ]
        )
        total_bet = bet_amount * len(betting_lines.split())

    inputs = {
        "expected_betting_lines": betting_lines, 
        "expected_total_bet": total_bet, 
        "expected_balance": balance, 
        "expected_bet_amount": bet_amount, 
        "expected_total_loss": total_bet
    }
    return inputs

# Check if the captured winning results are correct
def win_test(
    captured_slot_result, captured_winning_lines, 
    captured_winning_amount, info
):
    # Initialise expected results
    expected_winning_lines = None
    expected_winning_amount = None

    # Build a string of all winning betting lines chosen by the user
    lines = re.split(r"\r\n", captured_slot_result)
    for pos in str(info["expected_betting_lines"]).split():
        line_at_pos = lines[int(pos) - 1]

        # Checks if the line is a winning line
        winning_line_regex = (
            r"(\N{THUMBS UP SIGN}|\N{GRINNING FACE}|\N"
            r"{GRINNING FACE WITH STAR EYES}|\N{HUGGING FACE}) \| \1 \| \1"
        )
        if m := re.fullmatch(winning_line_regex, line_at_pos):
            if expected_winning_lines == None:
                expected_winning_lines = pos
                expected_winning_amount = (
                    symbol_value[emoji.demojize(m.group(1))]
                    * info["expected_bet_amount"]
                ) 
            else:
                expected_winning_lines += " " + pos
                expected_winning_amount += (
                    symbol_value[emoji.demojize(m.group(1))]
                    * info["expected_bet_amount"]
                ) 

    assert captured_winning_lines == expected_winning_lines
    if expected_winning_amount == None:
        assert captured_winning_amount == expected_winning_amount
        expected_winning_amount = 0
    else:
        assert captured_winning_amount == str(expected_winning_amount)
    
    return expected_winning_amount

# Check if the captured ending results are correct
def end_test(
    captured_total_bet, captured_bal_after_round, 
    inputs, expected_winning_amount
):
    assert captured_total_bet == str(inputs["expected_total_loss"])
    expected_bal_after_round = (
        inputs["expected_balance"] - inputs["expected_total_bet"]
        + expected_winning_amount
    )

    # Check that the slotmachine only displays the balance after the round 
    # when the balance is positive
    if expected_bal_after_round == 0:
        assert captured_bal_after_round == None
    else:
        assert captured_bal_after_round == str(expected_bal_after_round)
    return expected_bal_after_round

# Check if input prompts are correct. Test fails when concatenated outputs
# are not in the correct format
def request_inputs_test(child: pexpect.spawn, inputs, actual_round_output):
    child.expect(fr"{BET_PROMPT_RE}", timeout=3)
    actual_round_output += child.before + child.after
    child.send(f"{inputs['expected_bet_amount']}\n")

    child.expect(fr"{LINES_PROMPT_RE}", timeout=2)
    actual_round_output += child.before + child.after
    child.send(f"{inputs['expected_betting_lines']}\n")

    child.expect(fr"{BETTING_INFO_CONFIRMATION_RE}", timeout=2)
    assert child.match.group(1) == str(inputs['expected_total_bet'])
    assert child.match.group(2) == str(inputs['expected_betting_lines'])
    actual_round_output += child.before + child.after

    capture_pattern = (
        f"({SPIN_OUTCOME_RE})"
        f"(?:{WINNING_OUTCOME_RE})?"
        f"{LOST_OUTCOME_RE}"
        f"(?:{BALANCE_IS_POSITIVE_RE}|{BALANCE_IS_ZERO_RE})"
    )
    index = child.expect([capture_pattern, pexpect.TIMEOUT], timeout=2)
    captured_result = child.match
    
    if index == 1:
        pytest.fail("Round output is invalid")

    actual_round_output += child.before + child.after
    return captured_result, actual_round_output

# Spawn an interactive slot machine CLI instance and verify
# that it displays the correct input prompt
def spawn_slot_machine(inputs):
    child = pexpect.spawn("slotmachine", encoding='utf-8')
    child.expect(fr"{DEPOSIT_PROMPT_RE}", timeout=2)
    actual_round_output = child.before + child.after
    child.send(f"{inputs['expected_balance']}\n")

    child.expect(fr"{BALANCE_PROMPT_RE}", timeout=2)
    actual_round_output += child.before + child.after
    assert child.match.group(1) == str(inputs['expected_balance'])

    child.expect(fr"{START_GAME_PROMPT_RE}", timeout=2)
    actual_round_output += child.before + child.after
    child.send("\n")

    return child, actual_round_output

# Handle the case when another deposit prompt occured
def request_deposit_again_test(child: pexpect.spawn, actual_round_output):
    r2_inputs = None
    index = child.expect([fr"{DEPOSIT_PROMPT_RE}", pexpect.TIMEOUT], timeout=2)
    if index == 0:
        actual_round_output += child.after + child.before
        r2_inputs = user_input_generator(bal_equal_total_bet=False)
        child.send(f"{r2_inputs['expected_balance']}\n")
    return actual_round_output, r2_inputs

# Test if the program can terminate and returns all of the rounds' output
# for later testing
def terminate_slot_machine_test(
    child: pexpect.spawn, actual_round_output, 
    terminate
):
    child.expect(fr"{START_GAME_PROMPT_RE}", timeout=2)
    actual_round_output += child.before + child.after

    # Terminate the program
    if terminate:
        child.sendcontrol('d')
        child.expect_exact(pexpect.EOF, timeout=2)
        actual_round_output += child.before
    else:
        child.send('\n')
    return actual_round_output

# Check if the slotmachine's output matches with the expected output
# by calling helper functions
def run_slot_machine(
    inputs, desired_output, not_desired_output, 
    terminate, first_run=True, child=None
):
  # Loop ends when the rounds' desired output 
  # (i.e either a win or loss) is found
  while True:
    actual_round_output = ''
    if first_run:
        child, actual_round_output = spawn_slot_machine(inputs)

    # Testing the CLI's behaviour
    captured_result, actual_round_output = request_inputs_test(
        child, inputs, 
        actual_round_output
    )
    actual_round_output, r2_inputs = request_deposit_again_test(
        child, actual_round_output
    )
    actual_round_output = terminate_slot_machine_test(
        child, actual_round_output, 
        terminate
    )
    expected_winning_amount = win_test(
        captured_result.group(1), captured_result.group(2), 
        captured_result.group(3), inputs
    )
    bal_after_round = end_test(
        captured_result.group(4), captured_result.group(5), 
        inputs, expected_winning_amount
    )

    # Testing the format of all outputs produced by the CLI in this round
    if re.fullmatch(rf"{desired_output}", rf"{actual_round_output}"):
        print(actual_round_output)
        return child, bal_after_round, r2_inputs
    elif re.fullmatch(rf"{not_desired_output}", rf"{actual_round_output}"):
        # Round's output is valid format but isn't the desired one
        child.close()
        continue
    else:
        # Rounds' output doesn't match with any of the valid formats
        child.close()
        pytest.fail("Round output is invalid")