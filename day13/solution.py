import sys

def parse(lines: list[str]) -> tuple[int, list[int]]:
  timestamp = int(lines[0])
  ids = lines[1].split(',')
  ids = filter(lambda s: s != 'x', ids)
  ids = list(map(lambda v: int(v), ids))
  return timestamp, ids

def findBus(timestamp: int, ids: list[int]) -> int:
  def findDiff(id: int) -> int:
    return (((timestamp // id) + 1) * id - timestamp) % id

  min_id = ids[0]
  min_delta = findDiff(ids[0])
  for id in ids[1:]:
    delta = findDiff(id)
    if delta < min_delta:
      min_id, min_delta = id, delta
  return min_id * min_delta

filename = sys.argv[1] if len(sys.argv) == 2 else 'input.txt'
f = open(filename, 'r')

timestamp, ids = parse(f.readlines())
print(findBus(timestamp, ids))