
import time

def SelectAB(cond, A, B):
	return A if cond else B

class TimeStamp():
	def __init__(self, enable=True, name=None, echo=True):
		"""Initialize time stamp.
		param: enable		control on/off time stamp log
		param: name			name string of time stamp
		param: echo			print initialization message if True
		"""
		self.isEnable = enable
		self.procName = name
		self.procStart = 0
		self.subStart = 0
		if echo:
			sz = SelectAB(self.isEnable, "enabled", "disabled")
			print("TS[{}]: {}".format(name, sz))

	def ProcStart(self):
		"""
		"""
		self.procStart = 0
		if self.isEnable:
			self.procStart = time.time()
		return self.procStart

	def ProcEnd(self):
		elapsed = 0
		if self.isEnable:
			elapsed = time.time() - self.procStart
			print("TS[{}]: total {:.2f} sec elapsed.".format(self.procName, elapsed))
		return elapsed

	def SubStart(self):
		if self.isEnable:
			self.subStart = time.time()
		return self.subStart

	def SubEnd(self, strMesg):
		elapsed = 0
		if self.isEnable:
			elapsed = time.time() - self.subStart
			print("TS[{}]: {:.2f} sec elapsed.".format(strMesg, elapsed))
		return elapsed
