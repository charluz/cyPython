
import time

def SelectAB(cond, A, B):
	return A if cond else B

def getReturnTime(t, isMs):
	return SelectAB(isMs, t*1000.0, t)


class TimeStamp:
	def __init__(self, enable=True, name=None, echo=True, miliSec=False):
		"""Initialize time stamp.
		param: enable		control on/off time stamp log
		param: name			name string of time stamp
		param: echo			print initialization message if True
		"""
		self.isEnable = enable
		self.procName = name
		self.procStart = 0
		self.subStart = 0
		self.echo = echo
		self.miliSec = miliSec
		if self.echo:
			sz = SelectAB(self.isEnable, "enabled", "disabled")
			print("TS[{}]: {}".format(name, sz))

	def echoLog(self, enable):
		"""To enable/disable log print. enable=True/False
		"""
		self.echo = enable

	def ProcStart(self):
		"""
		"""
		self.procStart = 0
		if self.isEnable:
			self.procStart = time.time()
		return  getReturnTime(self.procStart, self.miliSec)

	def ProcEnd(self):
		elapsed = 0
		if self.isEnable:
			elapsed = time.time() - self.procStart
			retTime = getReturnTime(elapsed, self.miliSec)
			if self.echo:
				print("TS[{}]: total {:.4f} {}} elapsed.".format(self.procName, retTime, SelectAB(self.miliSec, "ms", "sec")))
		return retTime

	def SubStart(self):
		if self.isEnable:
			self.subStart = time.time()
		return getReturnTime(self.subStart, self.miliSec)

	def SubEnd(self, strMesg):
		elapsed = 0
		if self.isEnable:
			elapsed = time.time() - self.subStart
			retTime = getReturnTime(elapsed, self.miliSec)
			if self.echo:
				print("TS[{}]: {:.4f} {} elapsed.".format(strMesg, retTime, SelectAB(self.miliSec, "ms", "sec")))
		return retTime
