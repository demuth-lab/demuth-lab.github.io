---
layout: page
title: People
permalink: /people/
---

## Principal Investigator

<div class="pi-wrap">
  <img class="pi-photo" src="/assets/img/people/Demuth_Headshot.jpg" alt="Jeff Demuth">
  <div class="pi-text">
    <h3>Jeff Demuth</h3>
    <p><strong>Associate Professor, Department of Biology, University of Texas at Arlington</strong></p>

    <p>
      Jeff Demuth is an evolutionary geneticist studying how sex chromosomes and genome architecture shape behavioral responses to social conflict.
      His research integrates comparative genomics, regulatory evolution, and behavioral genetics in horned beetles and related systems.
    </p>

    <div class="pi-links">
      <a href="{{ site.data.links.scholar }}" target="_blank" rel="noopener" class="scholar-link">
        <i class="bi bi-mortarboard-fill" aria-hidden="true"></i> Google Scholar
      </a>

      <a href="https://orcid.org/0000-0002-0471-3679" target="_blank" rel="noopener" class="scholar-link">
        <i class="bi bi-link-45deg" aria-hidden="true"></i> ORCID
      </a>

      <a href="#" class="scholar-link" id="pi-email" data-user="jpdemuth" data-domain="uta.edu">
        <i class="bi bi-envelope-fill" aria-hidden="true"></i>
        Contact Me
      </a>
    </div>
  </div>
</div>

---

## Graduate Students

<div class="people-grid">
{% for person in site.data.people %}
  {% if person.level == "graduate" %}
    <div class="person-card">
      <img src="{{ person.photo }}" alt="{{ person.name }}">
      <h4>{{ person.name }}</h4>
      <p>{{ person.description }}</p>
    </div>
  {% endif %}
{% endfor %}
</div>

---

## Undergraduate Researchers

<div class="people-grid">
{% for person in site.data.people %}
  {% if person.level == "undergraduate" %}
    <div class="person-card">
      <img src="{{ person.photo }}" alt="{{ person.name }}">
      <h4>{{ person.name }}</h4>
      <p>{{ person.description }}</p>
    </div>
  {% endif %}
{% endfor %}
</div>

## Lab Alumni

{% assign alumni = site.data.people | where: "role", "Alumni" %}
{% assign group_order = "Postdocs|Graduate Students|Lab Managers|Undergraduate Students" | split: "|" %}

{% for group_name in group_order %}
  {% assign group_items = alumni | where: "alumni_group", group_name %}

  {% if group_items and group_items.size > 0 %}
### {{ group_name }}

<ul class="alumni-list">
  {%- comment -%}
  Sort: prefer most-recent first by year if present; otherwise name.
  Jekyll’s sort is ascending, so we sort then reverse for recency.
  {%- endcomment -%}

  {% assign with_year = group_items | where_exp: "p", "p.year" | sort: "year" | reverse %}
  {% assign with_years = group_items | where_exp: "p", "p.years" %}
  {% assign no_year = group_items | where_exp: "p", "p.year == nil and p.years == nil" | sort: "name" %}

  {%- comment -%}
  We can’t reliably sort ranges like "2011–2012" without extra parsing,
  so we keep them in the order they appear in the YAML file.
  If you want these sorted too, add alumni_sort: 2012 (end year) to those entries.
  {%- endcomment -%}

  {% for p in with_year %}
    <li class="alumni-row">
      <span class="alumni-name">{{ p.name }}</span>
      <span class="alumni-meta">
        {% if p.degree %}{{ p.degree }}{% endif %}
        {% if p.year %} {{ p.year }}{% endif %}
      </span>
      {% if p.linkedin %}
        <a class="alumni-linkedin" href="{{ p.linkedin }}" target="_blank" rel="noopener">LinkedIn</a>
      {% endif %}
    </li>
  {% endfor %}

  {% for p in with_years %}
    <li class="alumni-row">
      <span class="alumni-name">{{ p.name }}</span>
      <span class="alumni-meta">
        {% if p.degree %}{{ p.degree }}{% endif %}
        {% if p.years %} {{ p.years }}{% endif %}
      </span>
      {% if p.linkedin %}
        <a class="alumni-linkedin" href="{{ p.linkedin }}" target="_blank" rel="noopener">LinkedIn</a>
      {% endif %}
    </li>
  {% endfor %}

  {% for p in no_year %}
    <li class="alumni-row">
      <span class="alumni-name">{{ p.name }}</span>
      <span class="alumni-meta">
        {% if p.degree %}{{ p.degree }}{% endif %}
      </span>
      {% if p.linkedin %}
        <a class="alumni-linkedin" href="{{ p.linkedin }}" target="_blank" rel="noopener">LinkedIn</a>
      {% endif %}
    </li>
  {% endfor %}
</ul>
  {% endif %}
{% endfor %}



<script>
(function () {
  const el = document.getElementById("pi-email");
  if (!el) return;

  const user = el.getAttribute("data-user");
  const domain = el.getAttribute("data-domain");
  const addr = user + "@" + domain;

  el.addEventListener("click", function (e) {
    e.preventDefault();
    window.location.href = "mailto:" + addr;
  });
})();
</script>
