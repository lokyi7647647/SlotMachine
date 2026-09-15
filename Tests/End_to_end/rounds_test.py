"""
# tests / end to end / rounds test

Tests to ensure the gameplay is correct
"""

import pytest

from .slotmachine_helpers import (
    user_input_generator,
    run_slot_machine
)
from .expected_outputs import (
    CTRL_D_RE,
    RANDOM_ROUND_RE,
    COMPLETE_ROUND_WIN_RE,
    COMPLETE_ROUND_LOSS_RE,
    COMPLETE_ROUND_LOSS_WITH_DEPOSIT_EQUAL_TOTAL_BET,
    DEPOSIT_START_PROMPT_RE
)


@pytest.mark.repeat(3)
def test_round_win_when_deposit_not_equal_total_bet():
    inputs = user_input_generator(bal_equal_total_bet=False)

    # Find a winning round and test the produced output
    desired_output = (
        DEPOSIT_START_PROMPT_RE 
        + COMPLETE_ROUND_WIN_RE 
        + CTRL_D_RE
    )
    not_desired_output = (
        DEPOSIT_START_PROMPT_RE 
        + COMPLETE_ROUND_LOSS_RE 
        + CTRL_D_RE
    )
    child, *_ = run_slot_machine(inputs, desired_output, not_desired_output, terminate=True)
    child.close()

@pytest.mark.repeat(3)
def test_round_lose_when_deposit_not_equal_total_bet():
    inputs = user_input_generator(bal_equal_total_bet=False)

    # Find a losing round and test the produced output
    desired_output = DEPOSIT_START_PROMPT_RE + COMPLETE_ROUND_LOSS_RE + CTRL_D_RE
    not_desired_output = DEPOSIT_START_PROMPT_RE + COMPLETE_ROUND_WIN_RE + CTRL_D_RE
    child, *_ = run_slot_machine(inputs, desired_output, not_desired_output, terminate=True)
    child.close()

@pytest.mark.repeat(3)
def test_round_loss_when_deposit_equals_total_bet():
    inputs = user_input_generator(bal_equal_total_bet=True)

    # Find a losing round and test the produced output
    desired_output = DEPOSIT_START_PROMPT_RE + COMPLETE_ROUND_LOSS_WITH_DEPOSIT_EQUAL_TOTAL_BET + CTRL_D_RE
    not_desired_output = DEPOSIT_START_PROMPT_RE + COMPLETE_ROUND_WIN_RE + CTRL_D_RE
    child, *_ = run_slot_machine(inputs, desired_output, not_desired_output, terminate=True)
    child.close()

@pytest.mark.repeat(3)
def test_win_first_round_random_second_round():
    # First round
    inputs = user_input_generator(bal_equal_total_bet=False)
    desired_output = DEPOSIT_START_PROMPT_RE + COMPLETE_ROUND_WIN_RE
    not_desired_output = DEPOSIT_START_PROMPT_RE + COMPLETE_ROUND_LOSS_RE
    child, bal_after_round, *_ = run_slot_machine(inputs, desired_output, not_desired_output, terminate=False)

    # Second round
    inputs = user_input_generator(bal_equal_total_bet=False, balance=bal_after_round)
    child, *_ = run_slot_machine(inputs, RANDOM_ROUND_RE, not_desired_output=None, terminate=True, first_run=False, child=child)
    child.close()

@pytest.mark.repeat(3)
def test_lose_first_round_random_second_round():
    # First round
    inputs = user_input_generator(bal_equal_total_bet=False)
    desired_output = DEPOSIT_START_PROMPT_RE + COMPLETE_ROUND_LOSS_RE
    not_desired_output = DEPOSIT_START_PROMPT_RE + COMPLETE_ROUND_WIN_RE
    child, bal_after_round, *_ = run_slot_machine(inputs, desired_output, not_desired_output, terminate=False)

    # Second round
    inputs = user_input_generator(bal_equal_total_bet=False, balance=bal_after_round)
    child, *_ = run_slot_machine(inputs, RANDOM_ROUND_RE, not_desired_output=None, terminate=True, first_run=False, child=child)
    child.close()

@pytest.mark.repeat(3)
def test_lose_first_round_when_deposit_equal_total_bet_random_second_round():
    # First round
    inputs = user_input_generator(bal_equal_total_bet=True)
    desired_output = DEPOSIT_START_PROMPT_RE + COMPLETE_ROUND_LOSS_WITH_DEPOSIT_EQUAL_TOTAL_BET 
    not_desired_output = DEPOSIT_START_PROMPT_RE + COMPLETE_ROUND_WIN_RE
    child, *_, r2_inputs = run_slot_machine(inputs, desired_output, not_desired_output, terminate=False)

    # Second round
    child, *_ = run_slot_machine(r2_inputs, RANDOM_ROUND_RE, not_desired_output=None, terminate=True, first_run=False, child=child)
    child.close()





  
    

