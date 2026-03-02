---
title: "Publications"
---

<p class="lede">
Selected and complete publications. 
For the most up-to-date list, see 
<a target="_blank" rel="noopener" href="{{ site.data.links.scholar }}">
Google Scholar
</a>.
</p>

<div class="card">
  <h3>How to update</h3>
  <ol>
    <li>Quick/manual: edit <code>_data/publications.yml</code>.</li>
    <li>Recommended: export/update <code>data/publications.bib</code> (from Google Scholar) and run <code>scripts/bib2yaml.py</code> to regenerate <code>_data/publications.yml</code>.</li>
  </ol>
</div>

<ul class="pub-list">
{% assign pubs = site.data.publications %}
{% for p in pubs %}
  <li class="pub-item">

    <div class="pub-title">
      {{ p.title }}
    </div>

    <div class="pub-meta">
      {{ p.authors }} · {{ p.venue }} · {{ p.year }}
    </div>

    <div class="pub-links">
      {% if p.doi %}
        <a class="doi-link" href="https://doi.org/{{ p.doi }}" target="_blank" rel="noopener">DOI</a>
      {% endif %}
      {% if p.url %}
        <a class="pub-link" href="{{ p.url }}" target="_blank" rel="noopener">Link</a>
      {% endif %}
      {% if p.pdf %}
        <a class="pub-link" href="{{ p.pdf }}" target="_blank" rel="noopener">PDF</a>
      {% endif %}
    </div>

    {% if p.tags and p.tags.size > 0 %}
      <div class="pub-tags">
        Tags: {{ p.tags | join: ', ' }}
      </div>
    {% endif %}

  </li>
{% endfor %}
</ul>
