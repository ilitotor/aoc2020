
from typing import Tuple

def evaluateExpression(v1: int, op: str, v2: int)  -> int:
  if op == '*':
    return v1 * v2
  elif op == '+':
    return v1 + v2
  raise Exception('Invalid operator', op)

def parseInt(line: str, pos: int) -> Tuple[int, int]:
  if line[pos] not in '0123456789':
    raise Exception('Invalid state. Expected an int', line[pos])
  return int(line[pos]), pos + 1

def parseOperator(line: str, pos: int) -> Tuple[str, int]:
  if line[pos] not in '+*':
    raise Exception('Invalid state. Expected an operator', line[pos])
  return line[pos], pos + 1

def solveExpression(line: str, pos: int = 0) -> Tuple[int, int]:
  i = pos
  v1, i = solveExpression(line, i + 1) if line[i] == '(' else parseInt(line, i)

  while i < len(line) and line[i] != ')':
    op, i = parseOperator(line, i)
    v2, i = solveExpression(line, i + 1) if line[i] == '(' else parseInt(line, i)
    v1 = evaluateExpression(v1, op, v2)
  return v1, i+1

f = open('input.txt', 'r')
lines = f.read().splitlines()
lines = [line.replace(' ', '') for line in lines]
results = [solveExpression(line) for line in lines]
results = [result for result, _ in results]
print(sum(results))