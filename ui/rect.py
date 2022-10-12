from type import Vec2, Vec4


class Rect:
  __align  : int
  __border : int
  __outline: str

  __pos: Vec2
  __dim: Vec2

  __pad: Vec4
  __mar: Vec4

  def __init__(self):
    self.__align   = 0
    self.__border  = 0
    self.__outline = "╔╗╚╝║═"

    self.__pos = [0] * 2
    self.__dim = [0] * 2
    self.__pad = [0] * 4
    self.__mar = [0] * 4

  @property
  def align(self) -> int:
    return self.__align

  @align.setter
  def align(self, a: int):
    if not isinstance(a, int):
      raise TypeError("Invalid argument type for 'align', expected <int>, got {tp}")

    if a > 15 or a < 0:
      raise ValueError(f"Illegal 4-bit alignment value: {a}")

    self.__align = a

  @property
  def border(self) -> int:
    return self.__border

  @border.setter
  def border(self, b: int):
    if not isinstance(b, int):
      raise TypeError("Invalid argument type for 'border', expected <int>, got {tp}")

    if b > 15 or b < 0:
      raise ValueError(f"Illegal 4-bit border value: {b}")

    self.__border = b

  @property
  def outline(self) -> str:
    return self.__outline

  @outline.setter
  def outline(self, o: str):
    if not isinstance(o, str):
      raise TypeError(f"Invalid argument type for 'outline', expected <str>, got {type(o)}")

    if len(o) != 6:
      raise ValueError("Outline defininitition must have exactly 6 characters")
    
    self.__outline = o

  @property
  def pos(self) -> Vec2:
    return tuple(self.__pos)

  @pos.setter
  def pos(self, p: Vec2):
    if not isinstance(p, (tuple, list)):
      raise TypeError(f"Invalid argument type for 'pos', expected <tuple<int, int>>, got {type(p)}")

    if len(p) != 2:
      raise ValueError("Position must be a tuple of two values!")

    if not all(isinstance(i, int) for i in p):
      raise TypeError("All position values must be integers!")

    self.__pos = list(p)

  @property
  def dim(self) -> Vec2:
    return tuple(self.__dim)

  @dim.setter
  def dim(self, d: Vec2):
    if not isinstance(d, (tuple, list)):
      raise TypeError(f"Invalid argument type for 'dim', expected <tuple<int, int>>, got {type(d)}")

    if len(d) != 2:
      raise ValueError("Dimension must be a tuple of two values!")

    if not all(isinstance(i, int) for i in d):
      raise TypeError("All dimension values must be integers!")

    if not all(i > 0 for i in d):
      raise ValueError("Dimensions can only be positive integers!")

    self.__dim = list(d)

  @property
  def padding(self) -> Vec4:
    return tuple(self.__pad)

  @padding.setter
  def padding(self, p: Vec4):
    if not isinstance(p, (tuple, list)):
      raise TypeError(f"Invalid argument type for 'padding', expected <tuple<int, int, int, int>>, got {type(p)}")

    if len(p) != 4:
      raise ValueError("Four dimension padding values required!")

    if not all(isinstance(i, int) for i in p):
      raise TypeError("All padding values must be integers!")

    if not all(i >= 0 for i in p):
      raise ValueError("Padding values cannot be negative!")

    self.__pad = list(p)

  @property
  def margin(self) -> Vec4:
    return tuple(self.__mar)

  @margin.setter
  def margin(self, m: Vec4):
    if not isinstance(m, (tuple, list)):
      raise TypeError(f"Invalid argument type for 'margin', expected <tuple<int, int, int, int>>, got {type(m)}")

    if len(m) != 4:
      raise ValueError("Four dimension margin values required!")

    if not all(isinstance(i, int) for i in m):
      raise TypeError("All margin values must be integers!")

    if not all(i >= 0 for i in m):
      raise ValueError("Margin values cannot be negative!")

    self.__mar = list(m)

  @property
  def full_width(self) -> int:
    _, _, ml, mr = self.__mar
    _, _, pl, pr = self.__pad

    bl = int(bool(self.__border & 4))
    br = int(bool(self.__border & 8))

    return self.__dim[0] + ml + mr + pl + pr + bl + br

  @property
  def full_height(self) -> int:
    mt, md, _, _ = self.__mar
    pt, pd, _, _ = self.__pad

    bt = int(bool(self.__border & 1))
    bd = int(bool(self.__border & 2))

    return self.__dim[1] + mt + md + pt + pd + bt + bd

  def _render(self, c: list[str]) -> None:
    mt, md, ml, mr = self.__mar
    pt, pd, pl, pr = self.__pad
    
    bt = bool(self.__border & 1)
    bd = bool(self.__border & 2)
    bl = bool(self.__border & 4)
    br = bool(self.__border & 8)
    
    at = bool(self.__align & 1)
    ad = bool(self.__align & 2)
    al = bool(self.__align & 4)
    ar = bool(self.__align & 8)

    otl, otr, obl, obr, ov, oh = self.__outline

    w, h = self.__dim

    tw = self.full_width

    lines = []

    # top margin
    lines.extend([" " * tw] * mt)

    # top border
    if bt:
      tmp = ""

      tmp += " " * ml
      tmp += otl if bl else ""
      tmp += oh  * (w + pl + pr)
      tmp += otr if br else ""
      tmp += " " * mr

      lines.append(tmp)

    # top padding
    if pt:
      tmp = ""

      tmp += " " * ml
      tmp += ov  if bl else ""
      tmp += " " * (w + pl + pr)
      tmp += ov  if br else ""
      tmp += " " * mr

      lines.extend([tmp] * pt)

    # content
    space = h - len(c)

    top = 0 if (space < 0) or (at and not ad) else (space >> 1  if at == ad else space) # top filling space
    bot = 0 if (space < 0) or (ad and not at) else (space - top if at == ad else space) # bottom filling space

    content = [
      *([""] * top), # top filler
      *(c[:h]),      # content
      *([""] * bot), # bottom filler
    ]

    for line in content:
      tmp = line[:w]

      if al != ar:
        if al: tmp = tmp.ljust (w) # align left
        else : tmp = tmp.rjust (w) # align right
      else   : tmp = tmp.center(w) # align center

      tmp = " " * ml + (ov if bl else "") + " " * pl + tmp + \
            " " * pr + (ov if br else "") + " " * mr

      lines.append(tmp)

    # bottom padding
    if pd:
      tmp = ""

      tmp += " " * ml
      tmp += ov  if bl else ""
      tmp += " " * (w + pl + pr)
      tmp += ov  if br else ""
      tmp += " " * mr

      lines.extend([tmp] * pd)

    # bottom border
    if bd:
      tmp = ""

      tmp += " " * ml
      tmp += obl if bl else ""
      tmp += oh  * (w + pl + pr)
      tmp += obr if br else ""
      tmp += " " * mr

      lines.append(tmp)

    # bottom margin
    lines.extend([" " * tw] * md)

    return lines
