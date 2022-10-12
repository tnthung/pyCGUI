from enum import Enum


class Dir:
  TOP   = 0b0001
  DOWN  = 0b0010
  LEFT  = 0b0100
  RIGHT = 0b1000

  TD = TOP  | DOWN
  LR = LEFT | RIGHT

  ALL = TOP | DOWN | LEFT | RIGHT
