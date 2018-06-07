from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re, unicodedata

class PreProses(object):
	"""docstring for ClassName"""
	def __init__(self, dokumen):
		self.dokumen = dokumen

	def hasNumbers(self, inputString):
		return bool(re.search(r'\d', inputString))

	def stopword(self):
		factory = StopWordRemoverFactory()
		stopword = factory.create_stop_word_remover()
		filtering = []
		for artikel in self.dokumen:
			plus = stopword.remove(artikel.isi)
			filtering.append(plus)
		return filtering

	def stemming(self, dokumen):
		factory = StemmerFactory()
		stemmer = factory.create_stemmer()
		katadasar = []
		for artikel in dokumen:
			plus = stemmer.stem(unicodedata.normalize('NFKD', artikel).encode('ascii','ignore'))
			katadasar.append(plus)
		return katadasar

	def queryPreProses(self):
		factory = StopWordRemoverFactory()
		stopword = factory.create_stop_word_remover()
		query = []
		for word in self.dokumen:
			plus = stopword.remove(word)
			if plus != '':
				query.append(plus)

		for i, kata in enumerate(query):
			if kata == '':
				del query[i]

		factory_s = StemmerFactory()
		stemmer = factory_s.create_stemmer()
		katadasar_q = []
		for point in query:
			plus = stemmer.stem(point)
			katadasar_q.append(plus)

		return katadasar_q

	def normalisasi(self, dokumen):
		store = []
		for artikel in dokumen:
			split = artikel.split()
			split.sort()
			store.append(split) 

		factory = StopWordRemoverFactory()
		stopword = factory.create_stop_word_remover()
		store_n = []
		for x, sentence in enumerate(store):
			store_n.append([])
			for word in sentence:
				plus = stopword.remove(word)
				has = self.hasNumbers(plus)

				if plus != '' and \
				has == False and \
				'-' not in plus and \
				len(plus) <= 13 and \
				len(plus) >= 3:
					store_n[x].append(plus)

		for i, kalimat in enumerate(store_n):
			for j, kata in enumerate(kalimat):
				if kata == '':
					del store_n[i][j]
		return store_n

	def koleksi(self, dokumen):
		store = []
		for artikel in dokumen:
			store.extend(artikel)
		store = set(store)
		store = list(store)
		store.sort()
		return store