from codeforces_api import CodeforcesApi
import json

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

	def getNextContests(self):
		contests = self.api.contest_list()
		resp = []
		for contest in contests['result']:
			if contest['phase'] == 'BEFORE':
				resp.append(contest)
		return resp

class User:
	def __init__(self, handle):
		self.api = CodeforcesApi()
		self.handle = handle

	def getUserRating(self):
		resp = self.api.user_info([self.handle])
		if resp['status']:
			return resp['result'][0]['rating']
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

def getFormattedTime(seconds):
	minutes = int(seconds / 60)
	hours = 0
	days = 0
	resp = ""

	while minutes >= 60:
		hours += 1
		minutes -= 60

	while hours >= 24:
		days += 1
		hours -= 24

	if days > 0:
		resp += '{}d '.format(days)

	if minutes == 0:
		resp += '{}h '.format(hours)
	else:
		resp += '{}h {}m'.format(hours, minutes)

	return resp

if __name__ == '__main__':
	cf = CFWatcher()
	#sub = cf.getLastSubmission("jonatas57")
	#print(sub)
	contests = cf.getNextContests()

	for contest in contests:
		print(contest['name'])
		print(Contest().getFormattedTime(contest['durationSeconds']))
