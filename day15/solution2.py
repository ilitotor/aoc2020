from dataclasses import dataclass
import re

@dataclass
class Instruction:
  pass

@dataclass
class Mask(Instruction):
  mask: str

@dataclass
class Mem(Instruction):
  position: int
  value: int

def parse(lines: list[str]) -> list[Instruction]:
  instructions: list[Instruction] = []
  for line in lines:
    if line.startswith('mask'):
      instructions.append(Mask(line[7:]))
    elif line.startswith('mem'):
      reg_exp = re.compile(r'^mem\[(\d+)\]\s+=\s+(\d+)$')
      match = reg_exp.match(line)
      if match is None:
        raise Exception(f'Invalid instruction {line}.')
      instructions.append(Mem(int(match.group(1)), int(match.group(2))))
  return instructions

def getPositions(position: int, mask: str) -> list[int]:
  modified_position = list('{0:{fill}36b}'.format(position, fill='0'))
  for i, bit in enumerate(mask):
    if bit == 'X':
      modified_position[i] = 'X'
    elif bit == '1':
      modified_position[i] = '1'
    elif bit == '0':
      # doesn't change
      pass

  floating_bits = modified_position.count('X')
  if floating_bits == 0:
    return [position]

  output = []
  for i in range(2**floating_bits):
    bits_to_write = '{0:{fill}{size}b}'.format(i, fill='0', size=floating_bits)
    new_position = modified_position.copy()
    indexes_to_write = [i for i in range(len(modified_position)) if modified_position[i] == 'X']
    for j, bit in enumerate(bits_to_write):
      new_position[indexes_to_write[j]] = bit
    output.append(int(''.join(new_position)))
  return output

def run(instructions: list[Instruction]) -> int:
  mem: dict[int, int] = {}
  mask = ''
  for instruction in instructions:
    if type(instruction) is Mask:
      mask = instruction.mask
    elif type(instruction) is Mem:
      positions = getPositions(instruction.position, mask)
      for position in positions:
        print(f'mem[{position}] = {instruction.value}')
        mem[position] = instruction.value
  return sum(mem.values())


f = open('input.txt', 'r')

lines = f.read().split('\n')
instructions = parse(lines)
print(run(instructions))
