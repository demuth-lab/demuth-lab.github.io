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

<!-- Year Jump Dropdown -->
<div class="pub-year-jump">
  <label for="yearJump"><strong>Jump to year:</strong></label>
  <select id="yearJump" onchange="if(this.value) location.hash=this.value;">
    <option value="">Select…</option>

    {% assign years_csv = "" %}
    {% for p in pubs %}
      {% if p.year %}
        {% assign y = p.year | append: "" %}
        {% unless years_csv contains y %}
          {% assign years_csv = years_csv | append: y | append: "," %}
        {% endunless %}
      {% endif %}
    {% endfor %}
    {% assign years = years_csv | split: "," %}

    {% for y in years %}
      {% if y != "" %}
        <option value="#year-{{ y }}">{{ y }}</option>
      {% endif %}
    {% endfor %}
  </select>
</div>

{% assign current_year = "" %}

{% for p in pubs %}
  {% assign y = p.year | append: "" %}

  {% if y != current_year %}
    {% if current_year != "" %}
      </ul>
    {% endif %}

<h2 id="year-{{ y }}" class="pub-year">{{ y }}</h2>

<ul class="pub-list">

    {% assign current_year = y %}
  {% endif %}

  <li class="pub-item">
    <div class="pub-title">{{ p.title }}</div>

    <div class="pub-meta">
      {{ p.authors }} · <em>{{ p.venue }}</em>
    </div>

   <div class="pub-links">
      {% if p.doi %}
        {% if p.type == "preprint" %}
          <a class="doi-link" href="https://doi.org/{{ p.doi }}" target="_blank" rel="noopener">View Preprint</a>
        {% else %}
          <a class="doi-link" href="https://doi.org/{{ p.doi }}" target="_blank" rel="noopener">View Article</a>
        {% endif %}
      {% endif %}
    
      {% if p.pdf %}
        <a class="pub-link" href="{{ p.pdf }}" target="_blank" rel="noopener">Download PDF</a>
      {% endif %}
    
      {% if p.url %}
        <a class="pub-link" href="{{ p.url }}" target="_blank" rel="noopener">Link</a>
      {% endif %}
    
      {% if p.software and p.software.size > 0 %}
        {% for s in p.software %}
          <a class="pub-link" href="{{ s.url }}" target="_blank" rel="noopener">{{ s.label }}</a>
        {% endfor %}
      {% endif %}
</div>

    {% if p.tags and p.tags.size > 0 %}
      <div class="pub-tags">
        Tags: {{ p.tags | join: ', ' }}
      </div>
    {% endif %}
    
    {% if p.software and p.software.size > 0 %}
       <div class="pub-software">
          <span class="pub-subhead">Software:</span>
          {% for s in p.software %}
             <a class="pub-link" href="{{ s.url }}" target="_blank" rel="noopener">{{ s.label }}</a>
          {% endfor %}
       </div>
     {% endif %}
  </li>

{% endfor %}
</ul>
