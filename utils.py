from re import compile

NUMBER_OR_DOT_REGER = compile(r'^[0-9.]$')

def is_number_or_dot(string: str):
  return bool(NUMBER_OR_DOT_REGER.search(string))

def is_valid_number(string: str):
  try:
    float(string)
    return True
  except ValueError:
    return False