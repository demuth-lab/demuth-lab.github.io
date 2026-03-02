---
title: "Publications"
layout: default
---

<p class="lede">
Selected publications. For the most up-to-date list, see
<a target="_blank" rel="noopener" href="{{ site.data.links.scholar }}">
Google Scholar
</a>.
</p>

{% assign pubs = site.data.publications %}
{% assign current_year = "" %}

{% for p in pubs %}
  {% assign y = p.year | append: "" %}

  {% if y != current_year %}
    {% if current_year != "" %}
      </ul>
    {% endif %}

<h2 id="year-{{ y }}">{{ y }}</h2>

<ul class="pub-list">

    {% assign current_year = y %}
  {% endif %}

  <li class="pub-item">
    <div class="pub-title">{{ p.title }}</div>

    <div class="pub-meta">
      {{ p.authors }} · {{ p.venue }} · {{ p.year }}
    </div>

    <div class="pub-links">
      {% if p.doi %}
        <a href="https://doi.org/{{ p.doi }}" target="_blank" rel="noopener">DOI</a>
      {% endif %}
      {% if p.url %}
        <a href="{{ p.url }}" target="_blank" rel="noopener">Link</a>
      {% endif %}
      {% if p.pdf %}
        <a href="{{ p.pdf }}" target="_blank" rel="noopener">PDF</a>
      {% endif %}
    </div>
  </li>

{% endfor %}
</ul>
