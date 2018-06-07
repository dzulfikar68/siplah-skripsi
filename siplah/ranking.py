import math
import collections

class Ranking(object):
	"""docstring for Ranking"""
	def __init__(self, dokumen, koleksi):
		self.dokumen = dokumen
		self.koleksi = koleksi

	def bobotDokumen(self):
		# count dokumen awal
		count = [[0 for a in range(len(self.koleksi))] for b in range(len(self.dokumen))]
		for x, kol in enumerate(self.koleksi):
			for y, dok in enumerate(self.dokumen):
				for kata in dok:
					if kol==kata:
						count[y][x] = count[y][x] + 1
		return count

	def bobotQuery(self, query, koleksi):
		# count query
		count_q = [0 for a in range(len(koleksi))]
		for x, kol in enumerate(koleksi):
			for q in query:
				if kol==q:
					count_q[x] = count_q[x] + 1
		return count_q

	def bobotKata(self, bDokumen):
		# n
		plus = [[0 for a in range(len(self.dokumen))] for b in range(len(self.koleksi))]
		for x, koleksi in enumerate(bDokumen):
			for y, kol in enumerate(koleksi):
				if kol != 0:
					plus[y][x] = plus[y][x] + 1

		sum_number = [0 for a in range(len(self.koleksi))]
		for x, number in enumerate(plus):
			for num in number:
				sum_number[x] = sum_number[x] + num

		# log(N/n)
		n_n = [0 for a in range(len(self.koleksi))]
		summary = len(bDokumen)
		for x, n in enumerate(sum_number):
			n_n[x] = float(float(summary) / float(n))

		# IDF
		idf = [0 for a in range(len(self.koleksi))]
		for x, f in enumerate(n_n):
			idf[x] = math.log(f)
		return n_n

	def bobotKataQuery(self, bobot, jumlah, koleksi):
		query = [0 for a in range(len(koleksi))]
		for x, nilai in enumerate(jumlah):
			query[x] = nilai * bobot[x]
		return query

	def bobotKataDokumen(self, bobot, jumlah):
		dokumen = [[0 for a in range(len(self.koleksi))] for b in range(len(self.dokumen))]
		for x, dok in enumerate(self.dokumen):
			for y, nilai in enumerate(self.koleksi):
				dokumen[x][y] = jumlah[x][y] * bobot[y]
		return dokumen

	def vectorSpaceModel(self, query, dokumen, koleksi, artikel):
		# normalisasi query
		q_ = 0
		for x, nilai in enumerate(query):
			q_ = q_ + (nilai * nilai)
		q_ = float(math.sqrt(q_))

		# normalisasi dokumen
		doc_ = [0 for a in range(len(dokumen))]
		for x, dok in enumerate(dokumen):
			for nilai in dok:
				doc_[x] = doc_[x] + (nilai * nilai)
			doc_[x] = math.sqrt(doc_[x])

		q_doc_ = [[0 for a in range(len(koleksi))] for b in range(len(artikel))]
		for x, dok in enumerate(dokumen):
			for y, nilai_kata in enumerate(dok):
				q_doc_[x][y] = nilai_kata * query[y]

		# normalisasi sum tiap dokumen
		q__doc__ = [0 for a in range(len(artikel))]
		for i, dok in enumerate(q_doc_):
			for nilai in dok:
				q__doc__[i] = q__doc__[i] + nilai

		# RUMUS: q__doc__/|q_|.|doc_|
		ranking = [0 for a in range(len(artikel))]
		for j, dok in enumerate(q_doc_):
			for nilai in dok:
				ranking[j] = float(q__doc__[j] / (q_ * doc_[j]))
		return ranking

	def viewDokumen(self, container, ranking):
		rank = {}
		for i, identitas in enumerate(container):
			rank[ranking[i]] = str(identitas.id)

		r = collections.OrderedDict(sorted(rank.items(), reverse=True))
		return r