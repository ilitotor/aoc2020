from dataclasses import dataclass
from os import times
import sys
from typing import Callable

@dataclass
class Bus:
  id: int
  position: int

def parse(lines: list[str]) -> list[Bus]:
  ids = lines[1].split(',')
  return [Bus(int(v), i) for i, v in enumerate(ids) if v != 'x']

def findTimestamp(buses: list[Bus]) -> int:
  getId: Callable[[Bus], int] = lambda bus: bus.id
  max_bus = max(buses, key=getId)
  print(max_bus)
  timestamp: int = max_bus.id - max_bus.position
  buses_found = set()
  buses_found.add(max_bus.id)
  increment = max_bus.id
  while True:
    found = True
    for bus in buses:
      if (timestamp + bus.position) % bus.id == 0:
        if not bus.id in buses_found:
          print(f'{timestamp}  {bus.id}')
          buses_found.add(bus.id)
          increment *= bus.id
      else:
        found = False
        break
    if found:
      return timestamp
    timestamp += increment
  # Should never reach this point.
  raise Exception('Tem coisa errada aí!')

filename = sys.argv[1] if len(sys.argv) == 2 else 'input.txt'
f = open(filename, 'r')

ids = parse(f.readlines())
print(ids)
print(findTimestamp(ids))