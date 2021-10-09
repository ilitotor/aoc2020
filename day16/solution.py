from dataclasses import dataclass
from itertools import chain
import re

@dataclass
class Field:
  name: str
  interval1: tuple[int, int]
  interval2: tuple[int, int]

@dataclass
class Ticket:
  fields: list[int]

def parseFields(lines: list[str]) -> list[Field]:
  output = []
  reg_exp = re.compile(r'^([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)$')
  for line in lines:
    match = reg_exp.match(line)
    if match is None:
      return output
    output.append(Field(
      match.group(1),
      (int(match.group(2)), int(match.group(3))),
      (int(match.group(4)), int(match.group(5))),
    ))
  raise Exception('Invalid state')

def parseTicket(line: str) -> Ticket:
  return Ticket([int(v) for v in line.split(',')])

def isValidValue(value: int, fields: list[Field]) -> bool:
  def insideRange(field: Field) -> bool:
    return (
      field.interval1[0] <= value <= field.interval1[1] or
      field.interval2[0] <= value <= field.interval2[1]
    )
  return any(map(insideRange, fields))

f = open('input.txt', 'r')
lines = f.read().splitlines()
fields = parseFields(lines)
nearby_ticket_index = lines.index('nearby tickets:')
tickets = list(map(parseTicket, lines[nearby_ticket_index + 1:]))

# Invalid fields
all_values = chain.from_iterable([ticket.fields for ticket in tickets])
sum_invalid_fields = sum([v for v in all_values if not isValidValue(v, fields)])
print(f'Sum of invalid fields: {sum_invalid_fields}')