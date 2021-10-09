from dataclasses import dataclass
import re
import functools
import itertools

Ticket = list[int]

@dataclass
class Field:
  name: str
  interval1: tuple[int, int]
  interval2: tuple[int, int]

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

def isInRange(value: int, fields: list[Field]) -> list[Field]:
  def insideRange(field: Field) -> bool:
    return (
      field.interval1[0] <= value <= field.interval1[1] or
      field.interval2[0] <= value <= field.interval2[1]
    )
  return list(filter(insideRange, fields))

def filterInvalidTickets(tickets: list[Ticket], fields: list[Field]) -> list[Ticket]:
  def isValidTicket(ticket: Ticket, fields: list[Field]) -> bool:
    for value in ticket:
      if len(isInRange(value, fields)) == 0:
        return False
    return True
  return [ticket for ticket in tickets if isValidTicket(ticket, fields)]

def ticketByColumn(tickets: list[Ticket]) -> list[list[int]]:
  num_columns = len(tickets[0])
  output = []
  for column in range(num_columns):
    output.append([ticket[column] for ticket in tickets])
  return output

def matchingFields(values: list[int], fields: list[Field]) -> list[str]:
  for value in values:
    fields = isInRange(value, fields)
  return [field.name for field in fields]

def removeAmbiguity(matching_fields: list[list[str]]) -> list[str]:
  single_names = [name_list[0] for name_list in matching_fields if len(name_list) == 1]
  while len(single_names) < len(matching_fields):
    for name_list in matching_fields:
      if len(name_list) == 1:
        continue
      for name in name_list:
        if name in single_names:
          name_list.remove(name)
    single_names = [name_list[0] for name_list in matching_fields if len(name_list) == 1]
  return single_names

f = open('input.txt', 'r')
lines = f.read().splitlines()
fields = parseFields(lines)
nearby_ticket_index = lines.index('nearby tickets:')
tickets = list(map(parseTicket, lines[nearby_ticket_index + 1:]))
your_ticket_index = lines.index('your ticket:')
your_ticket = parseTicket(lines[your_ticket_index + 1])
print(f'Num field: {len(fields)}  Num tickets:{len(tickets)}')

tickets = filterInvalidTickets(tickets, fields)
tickets_by_column = ticketByColumn(tickets)
matching_fields = [matchingFields(values, fields) for values in tickets_by_column]
matching_fields = removeAmbiguity(matching_fields)

departure_fields = [i for i, field in enumerate(matching_fields) if 'departure' in field]

total = 1
for i in departure_fields:
  total *= your_ticket[i]
print(total)