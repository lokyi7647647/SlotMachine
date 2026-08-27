def is_input_digit(type, input, check_zero=True):
  if not input.isdigit():
    print(f"{type} must be only digit (i.e 0-9)")
    return False
  input = int(input)
  if input <= 0 and check_zero:
    print(f"{type} needs to be greater than 0.00")
    return False
  return True