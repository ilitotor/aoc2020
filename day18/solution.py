from collections import deque
from typing import Any, Deque

def evaluateTopExpression(stack: Deque[Any]):
  if len(stack) < 3 or stack[-2] not in '+*':
    return
  v1, op, v2 = stack.pop(), stack.pop(), stack.pop()
  if op == '*':
    stack.append(v1 * v2)
  elif op == '+':
    stack.append(v1 + v2)
  else:
    raise Exception('Invalid operator', v1, op, v2)

def solveExpression(line: str) -> int:
  print(line)
  stack = deque()
  for c in line:
    if c in '0123456789':
      stack.append(int(c))
      evaluateTopExpression(stack)
    elif c in '*+':
      stack.append(c)
    elif c == '(':
      stack.append(c)
    elif c == ')':
      value = stack.pop()
      if stack.pop() != '(':
        raise Exception('Invalid state')
      stack.append(value)
      evaluateTopExpression(stack)

  if len(stack) != 1:
    raise Exception('Invalid state')
  return stack.pop()

f = open('input.txt', 'r')
lines = f.read().splitlines()
lines = [line.replace(' ', '') for line in lines]
results = [solveExpression(line) for line in lines]
print(sum(results))