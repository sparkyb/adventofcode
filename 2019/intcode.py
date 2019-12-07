from enum import IntEnum


class Opcode(IntEnum):
  def __new__(cls, opcode, params):
    member = int.__new__(cls, opcode)
    member._value_ = opcode
    return member

  def __init__(self, opcode, params):
    self.params = params

  ADD = (1, 3)
  MUL = (2, 3)
  IN = (3, 1)
  OUT = (4, 1)
  JNZ = (5, 2)
  JZ = (6, 2)
  LT = (7, 3)
  EQ = (8, 3)
  HALT = (99, 0)


class ParamMode(IntEnum):
  POSITION = 0
  IMMEDIATE = 1


class NeedsInput(Exception):
  pass


class Intcode(list):
  def __init__(self, program, input=()):
    super().__init__(program)
    self.ip = 0
    self.input = list(input)
    self.output = []
    self.halted = False

  def _param(self, param, mode=ParamMode.POSITION):
    if mode == ParamMode.POSITION:
      param = self[param]
    return param

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
      modes = []
      params = []
      for i in range(opcode.params):
        try:
          mode = ParamMode(param_modes % 10)
        except ValueError:
          raise ValueError('Invalid param mode {} @ {}'.format(param_modes % 10,
                                                               self.ip))
        param_modes //= 10
        params.append(self[self.ip])
        modes.append(mode)
        self.ip += 1

      if opcode == Opcode.ADD:
        a = self._param(params[0], modes[0])
        b = self._param(params[1], modes[1])
        self[params[2]] = a + b
      elif opcode == Opcode.MUL:
        a = self._param(params[0], modes[0])
        b = self._param(params[1], modes[1])
        self[params[2]] = a * b
      elif opcode == Opcode.IN:
        if not self.input:
          self.ip -= 2  # rewind instruction pointer to re-run this opcode when we get input
          raise NeedsInput()
        self[params[0]] = self.input.pop(0)
      elif opcode == Opcode.OUT:
        output = self._param(params[0], modes[0])
        self.output.append(output)
        if return_output:
          return output
      elif opcode == Opcode.JNZ:
        cond = self._param(params[0], modes[0])
        dest = self._param(params[1], modes[1])
        if cond != 0:
          self.ip = dest
      elif opcode == Opcode.JZ:
        cond = self._param(params[0], modes[0])
        dest = self._param(params[1], modes[1])
        if cond == 0:
          self.ip = dest
      elif opcode == Opcode.LT:
        a = self._param(params[0], modes[0])
        b = self._param(params[1], modes[1])
        self[params[2]] = 1 if a < b else 0
      elif opcode == Opcode.EQ:
        a = self._param(params[0], modes[0])
        b = self._param(params[1], modes[1])
        self[params[2]] = 1 if a == b else 0
      elif opcode == Opcode.HALT:
        self.halted = True
    return None
