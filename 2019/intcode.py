import enum


class ParamType(enum.Enum):
  READ = enum.auto()
  WRITE = enum.auto()


class Opcode(enum.IntEnum):
  def __new__(cls, opcode, *param_types):
    member = int.__new__(cls, opcode)
    member._value_ = opcode
    return member

  def __init__(self, opcode, *param_types):
    self.param_types = param_types

  ADD = (1, ParamType.READ, ParamType.READ, ParamType.WRITE)
  MUL = (2, ParamType.READ, ParamType.READ, ParamType.WRITE)
  IN = (3, ParamType.WRITE)
  OUT = (4, ParamType.READ)
  JNZ = (5, ParamType.READ, ParamType.READ)
  JZ = (6, ParamType.READ, ParamType.READ)
  LT = (7, ParamType.READ, ParamType.READ, ParamType.WRITE)
  EQ = (8, ParamType.READ, ParamType.READ, ParamType.WRITE)
  RBO = (9, ParamType.READ)
  HALT = (99,)


class ParamMode(enum.IntEnum):
  POSITION = 0
  IMMEDIATE = 1
  RELATIVE = 2


class NeedsInput(Exception):
  pass


class Intcode(list):
  def __init__(self, program, input=()):
    super().__init__(program)
    self.ip = 0
    self.input = list(input)
    self.output = []
    self.rel_base = 0
    self.halted = False

  def __getitem__(self, index):
    if index >= len(self):
      return 0
    else:
      return super().__getitem__(index)

  def __setitem__(self, index, value):
    if index >= len(self):
      self.extend([0] * (index - len(self) + 1))
    super().__setitem__(index, value)

  def run(self, return_output=False):
    while not self.halted:
      opcode = self[self.ip]
      param_modes = opcode // 100
      opcode %= 100
      try:
        opcode = Opcode(opcode)
      except ValueError:
        raise ValueError('Invalid opcode {} @ {}'.format(opcode, self.ip))
      self.ip += 1
      params = []
      for param_type in opcode.param_types:
        try:
          mode = ParamMode(param_modes % 10)
        except ValueError:
          raise ValueError('Invalid param mode {} @ {}'.format(param_modes % 10,
                                                               self.ip))
        param_modes //= 10
        param = self[self.ip]
        if mode == ParamMode.RELATIVE:
            param += self.rel_base
        if param_type == ParamType.WRITE:
          if mode == ParamMode.IMMEDIATE:
            raise ValueError('Invalid mode for destination {!r} @ {}'.format(
                mode,
                self.ip))
        else:
          if mode != ParamMode.IMMEDIATE:
            param = self[param]
        params.append(param)
        self.ip += 1

      if opcode == Opcode.ADD:
        a, b, dest = params
        self[dest] = a + b
      elif opcode == Opcode.MUL:
        a, b, dest = params
        self[dest] = a * b
      elif opcode == Opcode.IN:
        dest = params[0]
        if not self.input:
          self.ip -= 2  # rewind instruction pointer to re-run this opcode when we get input
          raise NeedsInput()
        self[dest] = self.input.pop(0)
      elif opcode == Opcode.OUT:
        output = params[0]
        self.output.append(output)
        if return_output:
          return output
      elif opcode == Opcode.JNZ:
        cond, dest = params
        if cond != 0:
          self.ip = dest
      elif opcode == Opcode.JZ:
        cond, dest = params
        if cond == 0:
          self.ip = dest
      elif opcode == Opcode.LT:
        a, b, dest = params
        self[dest] = 1 if a < b else 0
      elif opcode == Opcode.EQ:
        a, b, dest = params
        self[dest] = 1 if a == b else 0
      elif opcode == Opcode.RBO:
        self.rel_base += params[0]
      elif opcode == Opcode.HALT:
        self.halted = True
    return None
