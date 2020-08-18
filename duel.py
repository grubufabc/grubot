from cf2 import *
import sys
import time
from threading import Thread
import sys

def getResult(hsub):
	h, sub = hsub
	return h, sub.verdict, sub.creationTimeSeconds

class Duel(Thread):
	def __init__(self, handles, link):
		Thread.__init__(self)
		self.handles = handles
		self.contId, self.probId = getProblemInfo(link)
		self.watcher = CFWatcher()
		print("Duelo {} {}".format(self.contId, self.probId), file=sys.stderr)
	
	def run(self):
		self.winner = ""

		while True:
			print(len(self.handles))
			subs = [(h, self.watcher.getLastSubmission(h)) for h in self.handles]

			result = list(map(getResult, filter(lambda sub: sub[1].problem.contestId == self.contId and sub[1].problem.index == self.probId, subs)))

			win = ""
			t = 0x3f3f3f3f3f3f

			for h, ver, sec in result:
				print(h, ver, sec, file=sys.stderr)
				if ver == 'OK' and sec < t:
					win = h

			if win != "":
				self.winner = win
				break
			print("ok", file=sys.stderr)
			time.sleep(1)
		print("{} win!".format(self.winner), file=sys.stderr)
		sys.exit()
