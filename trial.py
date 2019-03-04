# Form of a trial:
# [(a_1, b_1), (a_2, b_2), ...]
# Where the ordered pairs are in the rectangle bounded by (0,0) and (7,7), and represent valid knight moves.

import random

def isvalidmove(p1, p2):
	a1, b1 = p1
	a2, b2 = p2
	return set(abs(a1-a2), abs(b1-b2)) == set([1,2])

def generatevalidmoves(p):
	a, b = p
	return set([(a+2, b+1), (a+2, b-1), (a+1, b+2), (a+1, b-2), (a-1, b+2), (a-1, b-2), (a-2, b+1), (a-2, b-1)])

def generatenewtrial():
	squares = set( (i, j) for i in range(8) for j in range(8) if (i != 0 or j != 0))
	tr = [(0,0)]
	while True:
		m = generatevalidmoves(tr[-1])
		m.intersection_update(squares)
		if len(m) == 0: return tr
		newmove = random.choice(list(m))
		tr.append(newmove)
		squares.remove(newmove)

def modifytrial(oldtrial):
	"""
	10% chance of a given step from the start being allowed to mutate.
	Once one step mutates, the rest must be thrown away.
	"""
	squares = set( (i, j) for i in range(8) for j in range(8) if (i != 0 or j != 0))
	tr = [(0,0)]
	while random.random() > .1:
		if len(oldtrial) <= len(tr):
			return tr
		newmove = oldtrial[len(tr)]
		tr.append(newmove)
		squares.remove(newmove)
	while True:
		m = generatevalidmoves(tr[-1])
		m.intersection_update(squares)
		if len(m) == 0: return tr
		newmove = random.choice(list(m))
		tr.append(newmove)
		squares.remove(newmove)

grading = dict(((i, j), 1) for i in range(8) for j in range(8) if (i+j)%2 == 1)
def scoreTrial(tr):
	length = len(tr)
	if length < 64:
		return length
	else:
		if grading[tr[-1]] == 1:
			print("Seen", tr[-1])
		grading[tr[-1]] -= 1
		return 64 + grading[tr[-1]] + 1

TRIALS = [None]
def main():
	Trials = [generatenewtrial() for i in range(1000000)]
	while True:
		random.shuffle(Trials)
		Trials.sort(key=scoreTrial, reverse=True)
		Trials = Trials[:1000]
		TRIALS[0] = Trials
		print([len(tr) for tr in Trials])
		print("Yet to see", len([i for i in grading.items() if i[1]==1]), "possible finishes")
		NewTrials = []
		for oldtrial in Trials:
			for i in range(1000):
				NewTrials.append(modifytrial(oldtrial))
		Trials = NewTrials

def getproportions():
	total = 0
	perend = dict(((i, j), 0) for i in range(8) for j in range(8) if (i+j)%2 == 1)
	while True:
		trial = generatenewtrial()
		total += 1
		if len(trial)==64:
			perend[trial[-1]] += 1
			print("Seen %s at trial %s" %(trial[-1], total))
		if total % 10000000 == 0:
			yield total, perend

try:
	main()
#	for total, perend in getproportions():
#		print(total)
#		l = list(perend.items())
#		l.sort(key = lambda p: p[1], reverse=True)
#		for pair in l:
#			print(" : ".join(map(str, pair)))
except KeyboardInterrupt:
	print("Find the latest trials in the singleton list 'TRIALS'.")
	import code
	code.interact(local=globals())
