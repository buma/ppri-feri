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
    <div class="navbar navbar-fixed-top navbar-inverse">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href="${request.route_url('home')}">
		  Principi distributivnih
          </a>
	  <ul class="nav">
		  <li><a href="${request.route_url('home')}">Nevronske mreže</a></li>
	  </ul>
        </div>
      </div>
    </div>
    <div class="container">
      <div>

  % if request.session.peek_flash():
  <div id="flash">
    <% flash = request.session.pop_flash() %>
	% for message in flash:
	${message}<br>
	% endfor
  </div>
  % endif

    
    ${next.body()}

  </div>
  </div>
  
</body>
</html>

