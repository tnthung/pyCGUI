import os
import sys
import time


def set_terminal_size(col: int, row: int) -> None:
  os.system(f"mode {col},{row}")


def set_terminal_title(title: str) -> None:
  os.system(f"title {title}")
