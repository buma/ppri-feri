# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>
<%block name="extrajs">
</%block>
<%block name="extracss">
% for css in css_tags: 
	${css|n}
%endfor
<style>
#commits li img{ width:36px; height:36px; float:left; margin-right:8px; }
#commits li{ clear:left; margin-top:8px; }
#commits li .co{ display:block; }
</style>
</%block>

<h1>Changelog</h1>

<div id="commits">Loading...</div>

<script src=
"http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.3.3/underscore-min.js"
></script>
<script src=
	 	"http://cdnjs.cloudflare.com/ajax/libs/datejs/1.0/date.min.js"
		></script>
<script>
function github_commits(resp) {
  _.templateSettings.interpolate = /\{\{(.+?)\}\}/g;
  var template = _.template(
  '<li><img src={{a_url}}> <a class=co href={{url}}>{{msg}}</a> <a href={{u_url }}>{{user}}</a> dodal <time datetime={{date}}>{{h_date}}</time></li>'
  )
  , html = []
  , i
  , len = resp.data.length
  ;

  function _url(u) {
    return u.replace(/\/(api\.|repos\/|users\/)/g, '/').replace(/\/commits\//, '/commit/');
  }
  function _date(d) {
	  var dat = Date.parse(d);
	  return dat.toLocaleString();
  }

  for (i=0; i < len; i++) {
    var da = resp.data[i];
    html += template({
      msg : da.commit.message,
      url : _url(da.url),
      date: da.commit.author.date,
      h_date: _date(da.commit.author.date),
      user: da.author.login,
      u_url:_url(da.author.url),
      a_url:da.author.avatar_url
    });
  }

  document.getElementById('commits').innerHTML = '<ul>'+ html +'</ul>';
}
</script>
<script src=
"https://api.github.com/repos/buma/ppri-feri/commits?callback=github_commits&per_page=5"
></script>
