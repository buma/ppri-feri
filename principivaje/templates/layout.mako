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
		  <li><a href="${request.route_url('mlp')}">Nevronske mreže</a></li>
	  </ul>
        </div>
      </div>
    </div>
    <div class="container">
      <div>
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
	      ${flash("error")}
	      ${flash("success")}

    
    ${next.body()}

  </div>
  </div>
  % if request.registry.settings["env"] == "production":
	  <a title="Real Time Web Analytics" href="http://getclicky.com/100545333"><img alt="Real Time Web Analytics" src="//static.getclicky.com/media/links/badge.gif" border="0" /></a>
	  <script src="//static.getclicky.com/js" type="text/javascript"></script>
	  <script type="text/javascript">try{ clicky.init(100545333); }catch(e){}</script>
	  <noscript><p><img alt="Clicky" width="1" height="1" src="//in.getclicky.com/100545333ns.gif" /></p></noscript>
  %endif
  
</body>
</html>

