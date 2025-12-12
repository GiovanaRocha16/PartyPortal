<h1>Players</h1>
<ul>
% for p in players:
  <li>{{p.username}} - Score: {{p.score if hasattr(p, 'score') else 0}}</li>
% end
</ul>
