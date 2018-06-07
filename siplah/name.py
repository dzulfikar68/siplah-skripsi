from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from collections import Counter
import re

class Name(object):
	"""docstring for ClassName"""
	def __init__(self, final, centroid, indexing):
		self.final = final
		self.centroid = centroid
		self.indexing = indexing

	def finaly(self):
		name_grup = [[] for a in range(len(self.centroid))]
		for row in self.indexing:
			for index, (key, value) in enumerate(self.final.iteritems()):
				if row.key == (key):
					name_grup[value-1].append(row.kata)

		name_grup_final = []
		for x, bagian in enumerate(name_grup):
			word_counter = {}
			for word in bagian:
				if word in word_counter:
					word_counter[word] += 1
				else:
					word_counter[word] = 1
			popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
			top_3 = popular_words[:3]
			name_grup_final.append(top_3)

		return name_grup_final