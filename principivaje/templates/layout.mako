# -*- coding: utf-8 -*- 
<!DOCTYPE html>
<html lang="en">
  
  <head>
    <meta charset="utf-8">
  <title>${title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="/static/favicon.ico">
    <!-- Le styles -->
    <style>
      body { padding-top: 60px; /* 60px to make the container go all the way
      to the bottom of the topbar */ }
    </style>
  <%block name="extracss" />
  <%block name="extrajs" />
  <script type="text/javascript"
	    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js">
      </script>
    <![endif]-->
  </head>

<body>
    <div class="container">
    <div class="navbar navbar-inverse">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="${request.route_url('home')}">
		<abbr title="Principi porazdeljene in računalniške inteligence">PPRI</abbr>
          </a>
	  <ul class="nav">
		  <li><a href="${request.route_url('delta')}">Delta algoritem</a></li>
		  <li class="dropdown">
		  	<a href="#" class="dropdown-toggle" data-toggle="dropdown">
				Hopfield
				<b class="caret"></b>
			</a>
			<ul class="dropdown-menu">
				<li><a href="${request.route_url('hop')}">Stanja</a></li>
				<li><a href="${request.route_url('hop_learn')}">Učenje</a></li>
				<li><a href="${request.route_url('hop_energy')}">Energija</a></li>
			</ul>
			</li>
		  <li><a href="${request.route_url('mlp')}">Nevronske mreža</a></li>
		  <li><a href="${request.route_url('changes')}">Changelog</a></li>
	  </ul>
        </div>
      </div>
    </div>
    ${flash("error")}
    ${flash("success")}

    
    ${next.body()}
</div>
<footer class="footer">
<div class="container">
	<p class="pull-right"><a href="#">Na vrh</a></p>
	<p>The author reserves the right not to be responsible for the topicality, correctness, completeness or quality of the information provided. Liability claims regarding damage caused by the use of any information provided, including any kind of information which is incomplete or incorrect,will therefore be rejected.</p>
</div>

</footer>
<a href="https://github.com/buma/ppri-feri"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_gray_6d6d6d.png" alt="Fork me on GitHub"></a>
</body>
</html>

<%def name="flash(queue)">
	% if request.session.peek_flash(queue):
		<% flash = request.session.pop_flash(queue) %>
		% for message in flash:
			<div class="alert alert-${queue}">
				% if title in message:
					<h4>${message["title"]}</h4>
				% endif
				${message["body"]}
			</div>
		% endfor
	% endif
</%def>
