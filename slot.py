from typing import Callable, Generic, TypeVar


T = TypeVar("T")


class UnsetValueException(Exception):
  pass


class Slot(Generic[T]):
  def __init__(self) -> None:
    self.__cb : dict[str, Callable[[T], None]] = {}
    self.__val: T

  def bind(self, name: str, cb: Callable[[T], None]) -> None:
    self.__cb[name] = cb

  def unbind(self, name: str) -> None:
    if name in self.__cb.keys():
      del self.__cb[name]

  @property
  def value(self) -> T:
    if not hasattr(self, "__val"):
      raise UnsetValueException("Slot has never been set.")

    return self.__val

  @value.setter
  def value(self, new_val: T) -> None:
    self.__val = new_val

    for cb in self.__cb.values(): 
      cb(new_val)

  def __str__(self) -> str:
    return str(self.__val)

  def __repr__(self) -> str:
    return str(self.__val)
