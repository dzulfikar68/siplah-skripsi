				monah_nugraheni

				{% for key, value in summ.items() %}
					{% if (key|int == iterasi|int) %}
						<h3>kelompok: <strong>{{ container.query.filter_by(id=value).first().kunci1 }}</strong></h3>
					{% endif %}
				{% endfor %}

				  <table class="table">
				      <tr>
				      {% for rank in ranking %}
				        <th>Doc ke: {{ (jumlah + 1) - loop.index }}</th>
				      {% endfor %}
				      </tr>
				      <tr>
				      {% for rank in ranking %}
				        <td>{{ rank }}</td>
				      {% endfor %}
				      </tr>
				  </table>



					<div class="row">

						<button type="button" class="btn btn-info" data-toggle="collapse" data-target="#demo">Simple collapsible</button>
						<div id="demo" class="collapse">

							
							
						</div>

					</div>

				  	{% for rank in ranking %}
						{ y: {{ rank }}, label: "Doc:{{ (jumlah + 1) - loop.index }}" },
					{% endfor %}

				  	<p>=========================================================================</p>

					<h3>query:</h3>
					<p>{{ query }}</p>

					<h3>kata pada dokumen:</h3>
					{% for dokumen in normalisasi %}
						<p>{{ dokumen }}</p>
					{% endfor %}

					<p>=========================================================================</p>

					<h3>koleksi kata:</h3>
					<p>{{ koleksi }}</p>

					<h3>jumlah bobot query:</h3>
					<p>{{ bobot_q }}</p>

					<h3>jumlah bobot dokumen:</h3>
					<p>{{ bobot_doc }}</p>

					<p>=========================================================================</p>

					<h3>idf:</h3>
					<p>{{ bobot_kata }}</p>

					<h3>tf*idf query:</h3>
					<p>{{ bobot_kata_q }}</p>

					<h3>tf*idf dokumen:</h3>
					<p>{{ bobot_kata_doc }}</p>

					<p>=========================================================================</p>

					<h1>K-MEANS:</h1>
					<h3>{{ catatan_bobot }}</h3>
					<h3>{{ catatan_grup }}</h3>
					<h3>{{ centroid }}</h3>
					<h3>{{ kelompok }}</h3>

					Doc:{{ (jumlah + 1) - loop.index }}

					<button type="button" class="btn btn-info" data-toggle="collapse" data-target="#tabelproses">Simple collapsible</button>
			  	<div id="tabelproses" class="collapse">

					<div>
					  <h2>Tahapan Proses Metode</h2>
					  <ul class="nav nav-tabs">
					    <li class="active"><a data-toggle="tab" href="#frek">Frekuensi Kata</a></li>
					    <li><a data-toggle="tab" href="#bobot">Pembobotan Kata</a></li>
					    <li><a data-toggle="tab" href="#vsm">VSM</a></li>
					    <li><a data-toggle="tab" href="#kmeans">K-MEANS</a></li>
					  </ul>

					  <div class="tab-content">
					    <div id="frek" class="tab-pane fade in active">
					      <h3>Frekuensi Kata</h3>
					      	<p>Query</p>
					      	<p>
							{% for q in query %}
							    {{ loop.index }}<span>. </span>{{ q }}<br>
							{% endfor %}
							</p>

							<br>

							<p>List Kata Koleksi</p>

							<div class="outer">
							    <div class="inner">
							        <table>
							            <tr>
							                <th>Kata :</th>
							                {% for koleksi in koleksi %}
							                	<td>{{ koleksi }}</td>
							                {% endfor %}
							            </tr>
							        </table>
							    </div>
							</div>

							<br>

							<p>Frekuensi Kata pada Query</p>

							<div class="outer">
							    <div class="inner">
							        <table>
							            <tr>
							                <th>Kata :</th>
							                {% for q in query %}
							                	<td><strong>{{ q }}</strong></td>
							                {% endfor %}
							            </tr>
							            <tr>
							                <th>Frekuensi :</th>
							                {% for doc in bobot_q %}
							                {% if doc != 0 %}
							                <td>{{ doc }}</td>
							                {% endif %}
							                {% endfor %}
							            </tr>
							        </table>
							    </div>
							</div>

							<br>

							<p>Frekuensi Kata pada Dokumen</p>

							<div class="outer">
							    <div class="inner">
							        <table>
							            <tr>
							                <th>Kata :</th>
							                {% for koleksi in koleksi %}
							                	<td><strong>{{ koleksi }}</strong></td>
							                {% endfor %}
							            </tr>
							            {% for bobot_doc in bobot_doc %}
							            <tr>
							                <th>Doc ke: {{ loop.index }}</th>
							                {% for doc in bobot_doc %}
							                <td>{{ doc }}</td>
							                {% endfor %}
							            </tr>
							            {% endfor %}
							        </table>
							    </div>
							</div>				

					    </div>

					    <div id="bobot" class="tab-pane fade">
					      <h3>Pembobotan Kata</h3>
					      	<p>Query</p>
					      	<p>
							{% for q in query %}
							    {{ loop.index }}<span>. </span>{{ q }}<br>
							{% endfor %}
							</p>

							<br>

							<p>Bobot IDF</p>

							<div class="outer">
							    <div class="inner">
							        <table>
							            <tr>
							                <th>Kata :</th>
							                {% for koleksi in koleksi %}
							                	<td><strong>{{ koleksi }}</strong></td>
							                {% endfor %}
							            </tr>
							            <tr>
							                <th>IDF :</th>
							                {% for doc in bobot_kata %}
							                <td>{{ doc }}</td>
							                {% endfor %}
							            </tr>
							        </table>
							    </div>
							</div>

							<br>

							<p>Bobot Kata pada Query</p>

							<div class="outer">
							    <div class="inner">
							        <table>
							            <tr>
							                <th>Kata :</th>
							                {% for q in query %}
							                	<td><strong>{{ q }}</strong></td>
							                {% endfor %}
							            </tr>
							            <tr>
							                <th>Bobot :</th>
							                {% for doc in bobot_kata_q %}
							                {% if doc != 0 %}
							                <td>{{ doc }}</td>
							                {% endif %}
							                {% endfor %}
							            </tr>
							        </table>
							    </div>
							</div>

							<br>

							<p>Bobot Kata pada Dokumen</p>

							<div class="outer">
							    <div class="inner">
							        <table>
							            <tr>
							                <th>Kata :</th>
							                {% for koleksi in koleksi %}
							                	<td><strong>{{ koleksi }}</strong></td>
							                {% endfor %}
							            </tr>
							            {% for dokumen in bobot_kata_doc %}
							            <tr>
							                <th>Dok ke: {{ loop.index }}</th>
							                {% for doc in dokumen %}
							                <td>{{ doc }}</td>
							                {% endfor %}
							            </tr>
							            {% endfor %}
							        </table>
							    </div>
							</div>

							<br>							

					    </div>

					    <div id="vsm" class="tab-pane fade">
					      <h3>VSM</h3>
					      <p>Query</p>
					      	<p>
							{% for q in query %}
							    {{ loop.index }}<span>. </span>{{ q }}<br>
							{% endfor %}
							</p>

					      <p>Hasil Perangkingan yang ter-retrieve</p>

							<div class="outer">
							    <div class="inner">
							        <table>
							            <tr>
							                <th>ID Dok :</th>
							                {% for i, view in view_ranking.iteritems() %}
							                <td><strong>{{ view }}</strong></td>
							                {% endfor %}
							            </tr>
							            <tr>
							                <th>Nilai VSM :</th>
							                {% for i, view in view_ranking.iteritems() %}
							                <td>{{ '%0.8f' % i|float }}</td>
							                {% endfor %}
							            </tr>
							            <tr>
							                <th>Rank :</th>
							                {% for i, view in view_ranking.iteritems() %}
							                <td><strong>{{ loop.index }}</strong></td>
							                {% endfor %}
							            </tr>
							        </table>
							    </div>
							</div>

							<br>

							<div id="chartContainer2" style="height: 300px; width: 100%;"></div>
							<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>

							<br><br><br><br><br><br>

							<div id="chartContainer" style="height: 300px; width: 100%;"></div>
							<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>

							<br>
					    </div>
					    <div id="kmeans" class="tab-pane fade">
					      <h3>K-MEANS</h3>
					      <p>Query</p>
					      	<p>
							{% for q in query %}
							    {{ loop.index }}<span>. </span>{{ q }}<br>
							{% endfor %}
							</p>

							<br>

					      <p>nilai centroid tiap iterasi</p>

							<div class="outer">
							    <div class="inner">
							        <table>
							            <tr>
							                <th>centroid ke:</th>
							                {% for x in range(sum_kel) %}
							                	<td><strong>{{ loop.index }}</strong></td>
							                {% endfor %}
							            </tr>
							            {% for seq in catatan_bobot %}
							            <tr>
							                <th>iterasi ke: {{ loop.index }}</th>
							                {% for centroid in seq %}
							                <td>{{ '%0.8f' % centroid|float }}</td>
							                {% endfor %}
							            </tr>
							            {% endfor %}
							        </table>
							    </div>
							</div>

							<br>

							<p>posisi dokumen pada kelompok tiap iterasi</p>

							<div class="outer">
							    <div class="inner">
							        <table>
							            <tr>
							                <th>Dok ke:</th>
							                {% for i, view in view_ranking.iteritems() %}
							                	<td><strong>{{ loop.index }}</strong></td>
							                {% endfor %}
							            </tr>
							            {% for seq in catatan_grup %}
							            <tr>
							                <th>iterasi ke: {{ loop.index }}</th>
							                {% for nilai in seq %}
							                	<td>
							                	{% for n in nilai %}
							                	{% if n == 1 %}
							                		kel:{{ loop.index }}
							                	{% endif %}
							                	{% endfor %}
							                	</td>
							                {% endfor %}
							            </tr>
							            {% endfor %}
							        </table>
							    </div>
							</div>

							<br>

							<p>Hasil Pengelompokkan dokumen</p>

							<div class="outer">
							    <div class="inner">
							        <table>
							            <tr>
							                <th>ID Dok :</th>
							                {% for i, view in final_result.iteritems() %}
							                <td><strong>{{ i }}</strong></td>
							                {% endfor %}
							            </tr>
							            <tr>
							                <th>Nilai VSM :</th>
							                {% for i, view in final_result.iteritems() %}
							                <td>{{ view }}</td>
							                {% endfor %}
							            </tr>
							        </table>
							    </div>
							</div>

							<br>

							<div id="chartContainer3" style="height: 300px; width: 100%;"></div>
							<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>

					    </div>
					  </div>
					</div>
				    
			  	</div>

			  	name_group = {}
		count = 1
		for value in enumerate(centroid):
			for k, v in final_result.iteritems():
				if (count)==v:
					name_group[count] = k
					count = count + 1

		def finaly(self):
			name_grup = [[] for a in range(len(self.centroid))]
			name_grup2 = [[] for a in range(len(self.centroid))]
			for index, (key, value) in enumerate(self.final.iteritems()):
				for i, v in enumerate(self.centroid):
					if value==(i+1):
						pre = self.pre(self.dokumen.query.filter_by(id=key).first().isi)
						name_grup[i].extend(pre)
						name_grup2[i].append(pre)

			intersect = set().intersection(*name_grup)

			if intersect == set([]):
				name_grup_final = []
				for x, bagian in enumerate(name_grup):
					counts = Counter(bagian)
					name_grup_final.append(counts.most_common(2))

				return name_grup_final
			else:
				return intersect