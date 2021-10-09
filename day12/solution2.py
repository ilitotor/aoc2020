import sys
import re

Coordinate = tuple[str, int]

def parseInstructions(lines: list[str]) -> list[Coordinate]:
  reg_exp = re.compile('^([NSWELRF])(\d+)$')
  def parse(line: str) -> tuple[str, int]:
    res = reg_exp.match(line)
    if res is None:
      raise Exception('Could not parse the instruction')
    return res.group(1), int(res.group(2))
  return list(map(parse, lines))

def clockwiseRotation(direction: str, angle: int) -> str:
  directions = ['N', 'E', 'S', 'W']
  index = directions.index(direction)
  num_shifts: int = angle // 90
  new_index = (index + num_shifts) % len(directions)
  return directions[new_index]

def changeDirection(direction: str, instruction: str, value: int) -> str:
  if value % 90 != 0 or value > 270:
    raise Exception(f'Invalid value for instruction {instruction}{value}')
  if instruction == 'L':
    value = 360 - value
  return clockwiseRotation(direction, value)

def updateCoordinate(
  coordinate: Coordinate,
  direction: str,
  value: int
) -> tuple[str, int]:
  new_direction = coordinate[0]
  new_position = coordinate[1]
  if coordinate[0] == direction:
    new_position += value
  else:
    new_position -= value
    if new_position < 0:
      new_position *= -1
      new_direction = direction
  return (new_direction, new_position)

def move(
  latitude: Coordinate,
  longitude: Coordinate,
  direction: str,
  value: int
) -> tuple[tuple[str, int], tuple[str, int]]:
  if direction in ['S', 'N']:
    return updateCoordinate(latitude, direction, value), longitude
  elif direction in ['E', 'W']:
    return latitude, updateCoordinate(longitude, direction, value)
  raise Exception(f'Invalid instruction {direction}{value}')

def rotateWaypoint(
  waypoint_latitude: Coordinate,
  waypoint_longitude: Coordinate,
  instruction: str,
  value: int
) -> tuple[Coordinate, Coordinate]:
  latitude_direction = changeDirection(waypoint_latitude[0], instruction, value)
  latitude = (latitude_direction, waypoint_latitude[1])
  longitude_direction = changeDirection(waypoint_longitude[0], instruction, value)
  longitude = (longitude_direction, waypoint_longitude[1])
  if latitude_direction in ['E', 'W']:
    latitude, longitude = longitude, latitude
  return latitude, longitude

def moveShip(
  latitude: Coordinate,
  longitude: Coordinate,
  waypoint_latitude: Coordinate,
  waypoint_longitude: Coordinate,
  multiplier: int
) -> tuple[Coordinate, Coordinate]:
  latitude, longitude = move(
    latitude, longitude, waypoint_latitude[0], waypoint_latitude[1] * multiplier)
  latitude, longitude = move(
    latitude, longitude, waypoint_longitude[0], waypoint_longitude[1] * multiplier)
  return latitude, longitude

def getPosition(instructions: list[Coordinate]) -> int:
  waypoint_latitude: Coordinate = ('N', 1)
  waypoint_longitude: Coordinate = ('E', 10)
  latitude = ('N', 0)
  longitude = ('E', 0)
  for instruction, value in instructions:
    if instruction in ['R', 'L']:
      waypoint_latitude, waypoint_longitude = rotateWaypoint(
        waypoint_latitude, waypoint_longitude, instruction, value)
    elif instruction == 'F':
      latitude, longitude = moveShip(
        latitude, longitude, waypoint_latitude, waypoint_longitude, value)
    else:
      waypoint_latitude, waypoint_longitude = move(
        waypoint_latitude, waypoint_longitude, instruction, value)
    print(latitude, longitude, waypoint_latitude, waypoint_longitude)
  print('Final coordinates:', latitude, longitude)
  return latitude[1] + longitude[1]

filename = sys.argv[1] if len(sys.argv) == 2 else 'input.txt'
f = open(filename, 'r')

instructions = parseInstructions(f.read().splitlines())
print(getPosition(instructions))