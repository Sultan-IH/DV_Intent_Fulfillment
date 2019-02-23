#ideally we should not have this scenario, and have some form of loop to go back and check.
#but hey, hackathon
waitingUsers = []
matchedUsers= {}

def createMatches(userId):
	if userId in waitingUsers:
		return None
	elif size(waitingUsers)!= 0:
		matchedUser = waitingUsers.get(0)
		waitingUsers.remove(matchedUser)

		matchId = uuid()

		matchedUsers[userId] = matchId
		matchedUsers[matchedUser] = matchId
		return uuid()

def endMatches(userId):
	if userId not in matchedUsers:












