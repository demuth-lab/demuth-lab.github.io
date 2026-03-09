---
layout: default
title: Home
body-class: home
show_title: false
---

<section class="hero-banner">
  <div class="hero-banner-inner">
    <div class="hero-banner-text">
      <p class="hero-quote">
        “If one could conclude as to the nature of the Creator from a study of creation, it would appear that God has an inordinate fondness for stars and beetles.”
      <span class="hero-attrib"> – J. B. S. Haldane</span>
      </p>

      <div class="hero-actions">
        <a class="button secondary" href="{{ '/join/' | relative_url }}">Join the Lab</a>
        <a class="button secondary" href="{{ '/research/' | relative_url }}">Explore Research</a>
        <a class="button secondary" target="_blank" rel="noopener" href="{{ site.data.links.scholar }}">Google Scholar</a>
      </div>
      
    </div>
  </div>
</section>

<div class="section-title">
  <h2>Research themes</h2>
  <a class="muted" href="{{ '/research/' | relative_url }}">All research →</a>
</div>

<div class="cards">
  {% for c in site.data.research_cards %}
    <a class="card" href="{{ c.url | relative_url }}">
      <h3>{{ c.title }}</h3>
      <p>{{ c.blurb }}</p>
    </a>
  {% endfor %}
</div>

<div class="section-title">
  <h2>Featured papers</h2>
  <a class="muted" href="{{ '/publications/' | relative_url }}">All publications →</a>
</div>

<ul class="pub-list">
  {% assign pubs = site.data.publications %}
  {% for p in pubs limit:3 %}
    <li>
      <div class="pub-title">{{ p.title }}</div>
      <div class="pub-meta">{{ p.authors }} · {{ p.venue }} · {{ p.year }}</div>
      <div class="pub-links">
        {% if p.doi %}<a target="_blank" rel="noopener" href="https://doi.org/{{ p.doi }}">DOI</a>{% endif %}
        {% if p.url %}<a target="_blank" rel="noopener" href="{{ p.url }}">Link</a>{% endif %}
      </div>
    </li>
  {% endfor %}
</ul>

<div class="section-title">
  <h2>Latest news</h2>
  <a class="muted" href="{{ '/news/' | relative_url }}">All news →</a>
</div>

<div class="cards">
  {% assign items = site.news | sort: 'date' | reverse %}
  {% for n in items limit:3 %}
    <a class="card" href="{{ n.url | relative_url }}">
      <h3>{{ n.title }}</h3>
      <p class="muted">{{ n.date | date: "%b %-d, %Y" }}</p>
      <p>{{ n.summary | default: n.excerpt | strip_html | truncate: 120 }}</p>
    </a>
  {% endfor %}
  {% if items.size == 0 %}
    <div class="card"><h3>No news yet</h3><p>Add a post in <code>news/</code> to show updates here.</p></div>
  {% endif %}
</div>
