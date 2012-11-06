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

<h1>Nevronska mreža</h1>

<p>Skripta je namenjena preverjanju računanju nevronskih mrež z backpropagation.</p>

<p>Privzeti podatki so podatki za nevronsko mrežo na strani 23/25 na predavanjih.</p>

<p>Parametri \(i\),\(j\) in \(l\) so parametri uteži: \(w_{i,j}^{(l)}\) ki povejo za katero utež si želimo izračunati popravek. 
</p>


${form|n}
