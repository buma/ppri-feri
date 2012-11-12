# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>
<%block name="extrajs">
% for js in js_tags: 
	${js|n}
%endfor
</%block>
<%block name="extracss">
% for css in css_tags: 
	${css|n}
%endfor
</%block>

% if neural:

	<h1>Nevronska mreža</h1>

	<p>Skripta je namenjena preverjanju računanju nevronskih mrež z backpropagation.</p>

	<p>Trenutno deluje samo epohalno učenje</p>

	<p>Privzeti podatki so podatki za nevronsko mrežo na strani 23/25 na predavanjih.</p>

	<p>Parametri \(i\),\(j\) in \(l\) so parametri uteži: \(w_{i,j}^{(l)}\) ki povejo za katero utež si želimo izračunati popravek. 
	</p>

	<p>Uteži se vpišejo vse. Npr. če so v navodilih uteži \(w_2^{(2)} = \{0, -0.3, 0.8\}\)
		in je iz slike razvidno da so to indeksi 0,2 in 3 potem je potrebno to utež vpisati
		kot utež \( \{0,0,-0.3,0.8\} \) (Namesto indeksa 1 vpišemo 0)</p>
% elif delta:
	<h1>Učni algoritem delta</h1>
	
	<p>Skripta je namenjena preverjanju računanju učnega algoritma delta.</p>

	<p>Trenutno deluje epohalno in vzorčno učenje s MSE in CEE napako.</p>
	
	<p>Privzeti podatki so podatki za nalogo na strani 18/25 na predavanjih.</p>

% elif hopfield:
	<h1>Iskanje stabilnih stanj v Hopfieldovi mreži</h1>
	
	<p>Skripta je namenjena preverjanju računanju stabilnih stanj v hopfieldovi mreži.</p>

	<p>Trenutno deluje sinhrono učenje.</p>
	
	<p>Privzeti podatki so podatki za nalogo na strani 4 na predavanjih.</p>

	<p>Stvar je v bistvu zelo preprosta:</p>
	<ul>
		<li>vzamemo matriko uteži v tem primeru ima velikost 3x3</li>
		<li>vzamemo matriko vseh vhodov v tem primeru ima velikost 8x3 oz \(2^n \times n\) \(n\) je velikost uteži</li>
		<li>Matriki matrično pomnožimo (velikosti so \((8x3) \times (3x3)\)) in dobimo matriko \(v_i\) velikosti 8x3</li>
	</ul>
	<p>Sedaj moramo samo še matriko \(v_i\) pretvorit v \(y_i\) s pomočjo Funkcije 1 ali 2. Odvisno od navodil</p>
	
	<div class="alert alert-warning alert-block">
	<button type="button" class="close" data-dismiss="alert">×</button>
	<h4>Opozorilo</h4>

		<p>Formula za \(v_i\) je na predavanjih podana kot \(v_i=\sum_{i=1}^{n}w_{i j}y_j(t-1)\) jaz uporabljam \(v_i=\sum_{i=1}^{n}w_{i j}y_i(t-1)\), ker drugače nevem kako bi se \(y_j\) računal</p>
	</div>
	
	<p>Funkcija 1: $$y =  \left\{\begin{matrix} 0 & \mbox {if } v < 0, \\ 1 & \mbox{if } v > 0, \\ \text{enako kot prej} & \mbox{if } v=0\end{matrix}\right.$$</p>

	<p>Funkcija 2: $$y =  \left\{\begin{matrix} -1 & \mbox {if } v < 0, \\ +1 & \mbox{if } v > 0, \\ \text{enako kot prej} & \mbox{if } v=0\end{matrix}\right.$$</p>
% elif hopfield_learn:
	<h1>Učenje Hoppfieldove mreže</h1>

	<p>Mreža dobi vhode in se nato nauči matriko uteži</p>

	<p>Privzeti podatki so podani za nalogo na strani 8 na predavanjih.</p>
% elif hopfield_energy:
	<h1>Računanje energije Hopfieldove mreže</h1>

	<p>Mreža dobi vhode in matriko uteži in vrne Energijsko funkcijo</p>

	<p>Privzeti podatki so podani za nalogo na strani 10 na predavanjih.</p>

	<p>Pri vnosu uteži so predvidena cela števila. Matrika se pomnoži sama z \(\frac{1}{N}\)</p>
	<div class="alert alert-info alert-block">
		<button type="button" class="close" data-dismiss="alert">×</button>
		<h4>Info</h4>
		Napaka v skripti odpravljena.
	</div>
%endif


% if hopfield or delta:
	<div class="alert alert-info alert-block">
		<button type="button" class="close" data-dismiss="alert">×</button>
		<h4>V vednost</h4>
		Nekatere vrednosti niso enako kot na predavanjih ugotavljam ali je to zaradi kakšnih napak, ali pa zaradi zaokroževanja.
		Zaokroževalo bi se naj na <strong>6</strong> decimalk. 
		%if delta:
			Ta skripta zaokrožuje na <strong>3</strong> mesta po vsakem izračunu.
		%else:
			Zato skripta to tudi počne.
		%endif
	</div>

% endif


${form|n}

% if text_izhod:
	% for text in text_izhod:
		% if text.startswith("$"):
			<p>${text}</p>
		% else:
			${text|n}
		%endif
	% endfor
% endif

% if tabela:
	% if hopfield:
		<p><span class="badge badge-important">5</span> označuje stabilno stanje</p>
	% endif

	<table class="table table-stripped">
		<thead>
			<tr>
				% for th in tabela[0]:
					<th>${th}</th>
				% endfor
			</tr>
		</thead>
		<tbody>
			% for row in tabela[1:]:
				<tr>
					% for td in row:
						% if isinstance(td, dict):
							<td><span class="badge badge-important" title="Stabilno stanje">${td["val"]}</span></td>
						% else:
							<td>${td}</td>
						% endif

					% endfor
				</tr>
			% endfor

		</tbody>

	</table>
% endif
