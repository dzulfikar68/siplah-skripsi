from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from preproses import PreProses
from ranking import Ranking
from kelompok import Kelompok
from name import Name
import os, shutil, unicodedata, datetime

basedir = os.path.abspath(os.path.dirname(__file__))

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = \
'sqlite:////' + os.path.join(basedir, 'database.db')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['UPLOAD_FOLDER'] = os.path.realpath('.') + \
'/siplah/static/uploads'
application.config['MAX_CONTENT_PATH'] = 10000000
application.config['SECRET_KEY'] = '1234567890987654321'

db = SQLAlchemy(application)

class Artikel(db.Model):
	__tablename__ = 'artikel'
	id = db.Column(db.String(8), primary_key=True, unique=True)
	judul = db.Column(db.String(200))
	kunci1 = db.Column(db.String(20))
	kunci2 = db.Column(db.String(20))
	kunci3 = db.Column(db.String(20))
	isi = db.Column(db.Text)
	file = db.Column(db.String(200))

	def __init__(self, id, judul, kunci1, kunci2, kunci3, isi, file):
		self.id = id.upper()
		self.judul = judul.upper()
		self.kunci1 = kunci1.lower()
		self.kunci2 = kunci2.lower()
		self.kunci3 = kunci3.lower()
		self.isi = unicodedata.normalize('NFKD', isi).encode('ascii','ignore')
		self.file = file

	def __repr__(self):
		return '[%s, %s, %s, %s, %s, %s, %s]' % \
			(self.id, self.judul, self.kunci1, self.kunci2, self.kunci3, str(self.isi), self.file)

class Admin(db.Model):
	__tablename__ = 'admin'
	username = db.Column(db.String(10), primary_key=True)
	password = db.Column(db.String(10), unique=True)
	kelompok = db.Column(db.String(10))

	def __init__(self, username, password, kelompok):
		self.username = username
		self.password = password
		self.kelompok = kelompok
		
	def __repr__(self):
		return '[%s, %s, %s]' % (self.username, self.password, self.kelompok)

class Indexing(db.Model):
	__tablename__ = 'indexing'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	key = db.Column(db.String(50))
	kata = db.Column(db.String(50))

	def __init__(self, key, kata):
		self.key = key
		self.kata = kata
		
	def __repr__(self):
		return '[%s, %s]' % (self.key, self.kata)

class Koleksi(db.Model):
	__tablename__ = 'koleksi'
	kata = db.Column(db.String(50), primary_key=True)

	def __init__(self, kata):
		self.kata = kata
		
	def __repr__(self):
		return '[%s]' % (self.kata)

class BobotDoc(db.Model):
	__tablename__ = 'frekdoc'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	dok = db.Column(db.String(50))
	jumlah = db.Column(db.String(50))

	def __init__(self, dok, jumlah):
		self.dok = dok
		self.jumlah = jumlah
		
	def __repr__(self):
		return '[%s, %s]' % (self.dok, self.jumlah)

class BobotKata(db.Model):
	__tablename__ = 'bobotkol'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	koleksi = db.Column(db.String(50))

	def __init__(self, koleksi):
		self.koleksi = koleksi
		
	def __repr__(self):
		return '[%s]' % (self.koleksi)

class BobotKataDoc(db.Model):
	__tablename__ = 'bobotdoc'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	dok = db.Column(db.String(50))
	bobot = db.Column(db.String(50))

	def __init__(self, dok, bobot):
		self.dok = dok
		self.bobot = bobot
		
	def __repr__(self):
		return '[%s, %s]' % (self.dok, self.bobot)

@application.route('/home')
@application.route('/')
def index():
	return render_template('index.html')

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@application.route('/ranking', methods=['GET', 'POST'])
def ranking():
	if request.method == 'POST':
		time_past = datetime.datetime.now()
		container = Artikel.query.all()
		query_req = request.form['query']
		if query_req == '':
			return render_template('index.html', notif='query is empty, please fill the query')
		# session['query_req'] = query_req

		query = str(query_req)
		query = query.split()
		query.sort()
		query = PreProses(query)
		query = query.queryPreProses()
		# session['query'] = query

		db_koleksi = Koleksi.query.all()
		koleksi = []
		for row in db_koleksi:
			koleksi.append(str(row.kata))
		# session['koleksi'] = koleksi

		running = Ranking(query, koleksi)
		bobot_q = running.bobotQuery(query, koleksi)
		if 1 not in bobot_q:
			return render_template('index.html', \
				notif='The query you are looking for does not exist/ is not retrieved on the collection of all articles')
		# session['bobot_q'] = bobot_q

		db_bobot_doc = BobotDoc.query.all()
		bobot_doc = [[] for a in range(len(container))]
		for j, y in enumerate(container):
			for row in db_bobot_doc:
				if int(row.dok) == (j+1):
					bobot_doc[j].append(int(row.jumlah))
		# session['bobot_doc'] = bobot_doc

		db_bobot_kata = BobotKata.query.all()
		bobot_kata = []
		for row in db_bobot_kata:
			bobot_kata.append(float(row.koleksi))
		# session['bobot_kata'] = bobot_kata

		bobot_kata_q = running.bobotKataQuery(bobot_kata, bobot_q, koleksi)
		# session['bobot_kata_q'] = bobot_kata_q

		db_bobot_kata_doc = BobotKataDoc.query.all()
		bobot_kata_doc = [[] for a in range(len(container))]
		for j, y in enumerate(container):
			for row in db_bobot_kata_doc:
				if int(row.dok) == (j+1):
					bobot_kata_doc[j].append(float(row.bobot))
		# session['bobot_kata_doc'] = bobot_kata_doc
		
		ranking = running.vectorSpaceModel(bobot_kata_q, bobot_kata_doc, koleksi, container)
		# session['ranking'] = ranking

		view_ranking = running.viewDokumen(container, ranking)
		# session['view_ranking'] = view_ranking

		rank = list(view_ranking)

		if 0.0 in view_ranking:
			del view_ranking[0.0]
		jumlah_kel = Admin.query.first().kelompok
		kelompok = Kelompok(view_ranking, jumlah_kel)
		centroid = sorted(kelompok.centroidAwal(), reverse=True)

		####################################################################
		
		final_bobot = [0 for a in range(len(centroid))]
		grup = [[0 for a in range(len(centroid))] for b in range(len(rank))]
		final_grup = [[1 for a in range(len(centroid))] for b in range(len(rank))]
		catatan_bobot = []
		catatan_grup = []

		g_example = kelompok.kMeans(centroid)

		catatan_bobot.append(centroid)
		catatan_grup.append(g_example)

		while grup!=final_grup:
			grup = kelompok.kMeans(centroid)

			kel_index = [0 for a in range(len(rank))]
			for i, x in enumerate(grup):
			 	kel_index[i] = x.index(1) + 1

			jum_index = [0 for a in range(len(centroid))]
			for i, x in enumerate(kel_index):
				for j, y in enumerate(centroid):
					if x == (j+1):
						jum_index[j] = jum_index[j] + 1

			jum_grup = [0 for a in range(len(centroid))]
			for i, x in enumerate(jum_grup):
				for j, y in enumerate(rank):
					if kel_index[j] == (i+1):
						jum_grup[i] = jum_grup[i] + y

			for i, x in enumerate(final_bobot):
				final_bobot[i] = float(jum_grup[i] / jum_index[i])

			final_grup = kelompok.kMeans(final_bobot)
			centroid = final_bobot

			catatan_bobot.append(final_bobot)
			catatan_grup.append(final_grup)

		# session['catatan_bobot'] = catatan_bobot
		# session['catatan_grup'] = catatan_grup

		final_kelompok = [0 for a in range(len(rank))]
		for i, x in enumerate(final_grup):
			final_kelompok[i] = x.index(1) + 1

		final_result = {}
		for index, (key, value) in enumerate(view_ranking.iteritems()):
			final_result[value] = final_kelompok[index]

		# session['final_result'] = final_result

		chart_group = [0 for a in range(len(centroid))]
		for k, v in final_result.iteritems():
			hitung = 1
			for c in enumerate(centroid):
				if v==hitung:
					chart_group[hitung-1] = chart_group[hitung-1] + 1
				hitung = hitung + 1
		sum_chart = sum(chart_group)
		# session['chart_group'] = chart_group
		# session['sum_chart'] = sum_chart

		indexing = Indexing.query.all()
		name = Name(final_result, centroid, indexing)
		name_final = name.finaly()

		sum_kel=len(centroid)
		# session['sum_kel'] = sum_kel

		rank = len(rank)-1
		if (rank)==len(container)-1:
			rank = len(container)

		time_now = datetime.datetime.now()
		timer = time_now - time_past

		return render_template('ranking.html', query_req=query_req, \
			view_ranking=view_ranking, container=Artikel, \
			jumlah=len(container), rank=rank, \
			final_result=final_result, sum_kel=sum_kel, \
			chart_group=chart_group, name_final=name_final, \
			query=query, koleksi=koleksi, bobot_q=bobot_q, \
			bobot_doc=bobot_doc, bobot_kata=bobot_kata, bobot_kata_q=bobot_kata_q, \
			bobot_kata_doc=bobot_kata_doc, ranking=ranking, \
			catatan_bobot=catatan_bobot, catatan_grup=catatan_grup, \
			sum_chart=sum_chart, time=timer.total_seconds())
	else:
		return render_template('index.html')

# @application.route('/progress')
# def progress():
	# query_req = session['query_req']
	# koleksi = session.get('koleksi')
	# bobot_q = session.get('bobot_q')
	# bobot_doc = session.get('bobot_doc')
	# bobot_kata = session.get('bobot_kata')
	# bobot_kata_q = session.get('bobot_kata_q')
	# bobot_kata_doc = session.get('bobot_kata_doc')
	# ranking = session.get('ranking')
	# view_ranking = session.get('view_ranking')
	# catatan_bobot = session.get('catatan_bobot')
	# catatan_grup = session.get('catatan_grup')
	# final_result = session.get('final_result')
	# chart_group = session.get('chart_group')
	# sum_chart = session.get('sum_chart')
	# sum_kel = session.get('sum_kel')
	# return render_template('progress.html')

@application.route('/setting', methods=['GET', 'POST'])
def setting():
	if 'username' in session:
		admin = Admin.query.first()
		if request.method == 'POST':
			trying = request.form['kelompok']
			if trying.isnumeric() == False:
				return render_template('setting.html', admin=admin, warning='Contents should be numbers (1-9)')
			admin.kelompok = trying

			db.session.add(admin)
			db.session.commit()
			return redirect(url_for('admin', success='The Cluster have been saved'))
		else:
			return render_template('setting.html', admin=admin)
	else:
		return render_template('login.html', notif="Please login for administration session")

@application.route('/login', methods=['GET', 'POST'])
def login():
	admin = Admin.query.first()
	if request.method == 'POST':
		if request.form['username']==admin.username and \
			request.form['password']==admin.password:
			session['username'] = admin.username
			return redirect(url_for('admin', notif='Welcome to manage of the article'))
		else: 
			return render_template('login.html', danger="Please fill the username and password")
	else:
		return render_template('login.html')

@application.route('/logout')
def logout():
	session.pop('username', None)
	return render_template('index.html', success='Logout successful')

@application.route('/admin')
@application.route('/admin/<notif>')
def admin(notif=None):
	if 'username' in session:
		admin = Admin.query.first()
		container = Artikel.query.all()
		summary = len(container)
		container = reversed(container)
		return render_template('admin.html', \
			container=container, summary=summary, admin=admin, notif=notif)
	else:
		return render_template('login.html', notif="Please login for administration session")

@application.route('/create', methods=['GET', 'POST'])
def create():
	if 'username' in session:
		if request.method == 'POST':
			id = request.form['id']
			judul = request.form['judul']
			kunci1 = request.form['kunci1']
			kunci2 = request.form['kunci2']
			kunci3 = request.form['kunci3']
			isi = request.form['isi']
			file = request.files['file']

			if file.filename == '' or \
				isi == '' or \
				judul == '' or \
				id == '':
				return render_template('create.html', warning='Please fill the form (*), not empty', \
					id=id, judul=judul, kunci1=kunci1, kunci2=kunci2, kunci3=kunci3, isi=isi)

			dokumen = Artikel.query.all()

			for dok in dokumen:
				if str(id) == dok.id:
					# return render_template('untitled.html', example=dokumen)
					return render_template('create.html', warning='ID already exists', \
						id=id, judul=judul, kunci1=kunci1, kunci2=kunci2, kunci3=kunci3, isi=isi)

			for dok in dokumen:
				if str(secure_filename(file.filename)) == str(dok.file):
					return render_template('create.html', warning='PDF File already exists', \
						id=id, judul=judul, kunci1=kunci1, kunci2=kunci2, kunci3=kunci3, isi=isi)

			filename = application.config['UPLOAD_FOLDER'] + \
			'/' + secure_filename(file.filename)
			try:
				file.save(filename)
			except:
				return render_template('create.html', danger='File upload error occurred', \
					id=id, judul=judul, kunci1=kunci1, kunci2=kunci2, kunci3=kunci3, isi=isi)
			file_name = secure_filename(file.filename)
			artikel = Artikel(id, judul, kunci1, kunci2, kunci3, isi, file_name)
			db.session.add(artikel)
			db.session.commit()
			return redirect(url_for('admin', success='Articles successfully added'))
		else:
			return render_template('create.html')
	else:
		return render_template('login.html', notif="Please login for administration session")

@application.route('/view/<id>')
def view(id):
	if 'username' in session:
		artikel = Artikel.query.filter_by(id=id).first()
		return render_template('view.html', artikel=artikel)
	else:
		return render_template('login.html', notif="Please login for administration session")

@application.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
	if 'username' in session:
		artikel = Artikel.query.filter_by(id=id).first()
		dokumen = Artikel.query.all()
		if request.method == 'POST':
			artikel.id = request.form['id']
			artikel.judul = request.form['judul']
			artikel.kunci1 = request.form['kunci1']
			artikel.kunci2 = request.form['kunci2']
			artikel.kunci3 = request.form['kunci3']
			artikel.isi = request.form['isi']
			file = request.files['file']

			if file.filename != '':
				for dok in dokumen:
					if str(secure_filename(file.filename)) == str(dok.file):
						return redirect(url_for('edit', warning='PDF File already exists'))

				filename_old = application.config['UPLOAD_FOLDER'] + \
				'/' + secure_filename(artikel.file)
				os.remove(os.path.join(filename_old))

				filename_new = application.config['UPLOAD_FOLDER'] + \
				'/' + secure_filename(file.filename)
				try:
					file.save(filename_new)
				except:
					return redirect(url_for('edit', danger='File upload error occurred'))
				
				artikel.file = secure_filename(file.filename)

			db.session.add(artikel)
			db.session.commit()
			return redirect(url_for('admin', success='Articles successfully edited'))
		else:
			return render_template('edit.html', artikel=artikel)
	else:
		return render_template('login.html', notif="Please login for administration session")

@application.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
	if 'username' in session:
		artikel = Artikel.query.filter_by(id=id).first()
		if request.method == 'POST':
			filename = application.config['UPLOAD_FOLDER'] + \
				'/' + artikel.file
			os.remove(os.path.join(filename))
			db.session.delete(artikel)
			db.session.commit()
			return redirect(url_for('admin', success='Articles successfully removed'))
		else:
			return render_template('delete.html', artikel=artikel)
	else:
		return render_template('login.html', notif="Please login for administration session")

@application.route('/update')
def update():
	container = Artikel.query.all()
	preproses = PreProses(container)
	stopword = preproses.stopword()
	stemming = preproses.stemming(stopword)
	normalisasi = preproses.normalisasi(stemming)
	koleksi = preproses.koleksi(normalisasi)

	rank_store = Ranking(normalisasi, koleksi)
	bobot_doc = rank_store.bobotDokumen()
	bobot_kata = rank_store.bobotKata(bobot_doc)
	bobot_kata_doc = rank_store.bobotKataDokumen(bobot_kata, bobot_doc)

	Koleksi.query.delete()
	Indexing.query.delete()
	BobotDoc.query.delete()
	BobotKata.query.delete()
	BobotKataDoc.query.delete()

	key_id = []
	for x in container:
		key_id.append(str(x.id))

	for i, dokumen in enumerate(normalisasi):
		for kata in dokumen:
			key = key_id[i]
			indexing_db = Indexing(key, kata)
			db.session.add(indexing_db)
	db.session.commit()

	for kata in koleksi:
		koleksi_db = Koleksi(kata)
		db.session.add(koleksi_db)
	db.session.commit()

	for i, dokumen in enumerate(bobot_doc):
		for kata in dokumen:
			index = str(i+1)
			bobot_doc_db = BobotDoc(index, kata)
			db.session.add(bobot_doc_db)
	db.session.commit()

	for kata in bobot_kata:
		bobot_kata_db = BobotKata(kata)
		db.session.add(bobot_kata_db)
	db.session.commit()

	for i, dokumen in enumerate(bobot_kata_doc):
		for kata in dokumen:
			index = str(i+1)
			bobot_kata_doc_db = BobotKataDoc(index, kata)
			db.session.add(bobot_kata_doc_db)
	db.session.commit()
	return redirect(url_for('admin', success='Articles successfully updated'))

@application.route('/deleteall')
def deleteall():
	Artikel.query.delete()
	db.session.commit()

	folder = 'siplah/static/uploads'
	for the_file in os.listdir(folder):
	    file_path = os.path.join(folder, the_file)
	    os.unlink(file_path)
	return redirect(url_for('admin', success='Articles successfully cleared'))

if __name__ == '__main__':
	application.run(debug=True)