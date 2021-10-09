from typing import List, Tuple, Set

def createDimension(
  lines: List[str], size: Tuple[int, int, int]
) -> List[List[List[bool]]]:
  output = [[[False for _ in range(size[0])] for _ in range(size[1])] for _ in range(size[2])]
  x_start = (size[0] - len(lines[0])) // 2
  y_start = (size[1] - len(lines)) // 2
  z_start = (size[2] - 1) // 2
  for y in range(len(lines)):
    for x in range(len(lines[y])):
      output[z_start][y + y_start][x + x_start] = lines[y][x] == '#'
  return output

def countActiveNeighbors(
  matrix: List[List[List[bool]]],
  coordinate: Tuple[int, int, int]
) -> int:
  c = 0
  x, y, z = coordinate[0], coordinate[1], coordinate[2]
  for zi in range(max([0, z-1]), min(len(matrix), z+2)):
    for yi in range(max([0, y-1]), min(len(matrix[z]), y+2)):
      for xi in range(max([0, x-1]), min(len(matrix[z][y]), x+2)):
        if matrix[zi][yi][xi]:
          c += 1
  if matrix[z][y][x]:
    c -= 1
  return c

def updateStatus(
  matrix: List[List[List[bool]]],
  coordinate: Tuple[int, int, int]
) -> bool:
  x, y, z = coordinate[0], coordinate[1], coordinate[2]
  active_neighbors = countActiveNeighbors(matrix, coordinate)
  if matrix[z][y][x]:
    return 2 <= active_neighbors <= 3
  else:
    return active_neighbors == 3

def updateCycle(matrix: List[List[List[bool]]]):
  updateList: Set[Tuple[int, int, int]] = set()
  for z in range(len(matrix)):
    for y in range(len(matrix[z])):
      for x in range(len(matrix[z][y])):
        if matrix[z][y][x] != updateStatus(matrix, (x, y, z)):
          updateList.add((x, y, z))
  for x, y, z in updateList:
    matrix[z][y][x] = not matrix[z][y][x]

def printMatrix(matrix: List[List[List[bool]]]):
  for z_slice in matrix:
    for y_slice in z_slice:
      out = ''.join(map(lambda b: '#' if b else '.', y_slice))
      print(out)
    print()

def countActive(matrix: List[List[List[bool]]]) -> int:
  c = 0
  for z_slice in matrix:
    c += sum([y_slice.count(True) for y_slice in z_slice])
  return c

f = open('input.txt', 'r')
lines = f.read().splitlines()
matrix = createDimension(lines, (20, 20, 13))
cycles = 6
for _ in range(cycles):
  updateCycle(matrix)
print(f'Active cubes: {countActive(matrix)}')