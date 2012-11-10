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
	
	<div class="alert alert-warning alert-block">
	<button type="button" class="close" data-dismiss="alert">×</button>
	<h4>Opozorilo</h4>

		<p>>Formula za \(v_i\) je na predavanjih podana kot \(v_i=\sum_{i=1}^{n}w_{i j}y_j(t-1)\) jaz uporabljam \(v_i=\sum_{i=1}^{n}w_{i j}y_i(t-1)\), ker drugače nevem kako bi se \(y_j\) računal</p>
	</div>

%endif

% if hopfield is None:

<div class="alert alert-info alert-block">
	<button type="button" class="close" data-dismiss="alert">×</button>
	<h4>V vednost</h4>
	Nekatere vrednosti niso enako kot na predavanjih ugotavljam ali je to zaradi kakšnih napak, ali pa zaradi zaokroževanja.
	Namreč nisem še ugotovil na kakšen način se bi naj zaokroževalo. Včasih sta 2 mesti včasih 3...
	%if delta:
		Ta skripta zaokrožuje na <strong>3</strong> mesta po vsakem izračunu.
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

% if hopfield:
	<p><span class="badge badge-important">5</span> označuje stabilno stanje</p>
% endif

% if tabela:
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
