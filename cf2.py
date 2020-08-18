from codeforces_api import CodeforcesApi

class CFObject():
	def __init__(self, obj):
		self.__dict__ = obj

class Problem(CFObject):
	def __init__(self, obj):
		CFObject.__init__(self, obj)

class Submission(CFObject):
	def __init__(self, obj):
		CFObject.__init__(self, obj)
		self.problem = Problem(self.problem)

	def __str__(self):
		s = "Submission {}\n{} - {}\n{}".format(self.id, self.problem.index, self.problem.name, self.verdict)
		return s

	def isAccepted(self):
		return self.verdict == "OK"

class CFWatcher:
	def __init__(self):
		self.api = CodeforcesApi()
	
	def getLastSubmission(self, handle):
		resp = self.api.user_status(handle, start=1, count=1)
		if resp['status']:
			return Submission(resp['result'][0])
		else:
			return None

def getProblemInfo(link):
	probId = ""
	contId = 0

	for c in link:
		if c >= '0' and c <= '9':
			contId *= 10
			contId += int(c)
		elif c >= 'A' and c <= 'Z':
			probId = c
	
	return contId, probId

if __name__ == '__main__':
	cf = CFWatcher()
	sub = cf.getLastSubmission("jonatas57")
	print(sub)
