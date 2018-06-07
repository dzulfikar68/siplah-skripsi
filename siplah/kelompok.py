import random
import math

class Kelompok(object):
	"""docstring for Kelompok"""
	def __init__(self, ranking, jumlah):
		self.ranking = ranking
		self.jumlah = int(jumlah)
	
	def centroidAwal(self):
		summary = self.jumlah
		rank = list(self.ranking)
		centroid = []
		secure_random = random.SystemRandom()
		i=0
		if len(rank)<summary:
			summary = len(rank)
		while i<summary:
			rand = secure_random.choice(rank)
			if rand not in centroid:
				centroid.append(rand)
				i = i+1
		return centroid

	def kMeans(self, centroid):
		rank = list(self.ranking)
		kel = [[0 for a in range(len(centroid))] for b in range(len(rank))]
		for i, x in enumerate(rank):
			for j, y in enumerate(centroid):
				kurangi = x - y
				pangkat = kurangi * kurangi
				kel[i][j] = math.sqrt(pangkat)

		grup = [[0 for a in range(len(centroid))] for b in range(len(rank))]
		for i, x in enumerate(kel):
		 	minimal = min(x)
		 	for j, y in enumerate(x):
		 		if y == minimal:
		 			grup[i][j] = 1
		 		else:
		 			grup[i][j] = 0
		return grup