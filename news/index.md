---
title: "News"
---

<p class="lede">Updates from the lab: papers, awards, outreach, and talks.</p>

{% assign items = site.news | sort: 'date' | reverse %}
{% if items.size == 0 %}
  <div class="card"><h3>No posts yet</h3><p>Add Markdown files to the <code>news/</code> folder to show updates.</p></div>
{% endif %}

<ul class="pub-list">
  {% for n in items %}
    <li>
      <div class="pub-title"><a href="{{ n.url | relative_url }}">{{ n.title }}</a></div>
      <div class="pub-meta">{{ n.date | date: "%B %-d, %Y" }}</div>
      {% if n.summary %}<div class="muted" style="margin-top:6px;">{{ n.summary }}</div>{% endif %}
    </li>
  {% endfor %}
</ul>
