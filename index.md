---
layout: default
show_title: false
---

<section class="hero">
  <div class="hero-grid">
    <div>
      <h1>Evolutionary genetics and genomics</h1>
      <p>We study how genes and genomes evolve to generate population differences and, ultimately, new species. Most of our experimental work uses flour beetles (<em>Tribolium</em>), and we combine experimental and computational approaches.</p>
      <div class="hero-actions">
        <a class="button primary" href="{{ '/join/' | relative_url }}">Join the Lab</a>
        <a class="button secondary" href="{{ '/research/' | relative_url }}">Explore Research</a>
        <a class="button" target="_blank" rel="noopener" href="{{ site.data.links.scholar }}">Google Scholar</a>
      </div>
      <p class="muted" style="margin-top:10px;">Based at UT Arlington · Recruiting PhD students, postdocs, and undergraduates.</p>
    </div>
    <div class="card">
      <h3>Quick links</h3>
      <p><strong>Prospective trainees:</strong> start with <a href="{{ '/join/' | relative_url }}">Join the Lab</a>.</p>
      <p><strong>Collaborators:</strong> see <a href="{{ '/research/' | relative_url }}">Research themes</a> and <a href="{{ '/publications/' | relative_url }}">Publications</a>.</p>
      <p><strong>Resources:</strong> data/code/protocol links on <a href="{{ '/resources/' | relative_url }}">Resources</a>.</p>
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
  {% assign pubs = site.data.publications | sort: 'year' | reverse %}
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
