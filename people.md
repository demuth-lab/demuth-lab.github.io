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

---

## Lab Alumni

{% assign alumni = site.data.people | where: "role", "Alumni" %}
{% assign group_order = "Postdocs|Graduate Students|Lab Managers|Undergraduate Honors Theses|Undergraduate Students" | split: "|" %}

{% for group_name in group_order %}
  {% assign group_items = alumni | where: "alumni_group", group_name %}

  {% if group_items.size > 0 %}
<h3>{{ group_name }}</h3>

<ul class="alumni-list">
  {%- comment -%}
  Sort by year when present (ascending), then reverse by printing in reverse order.
  No where_exp needed.
  {%- endcomment -%}

  {% assign items_sorted = group_items | sort: "year" %}

  {% for p in items_sorted reversed %}
    <li class="alumni-row">
      <span class="alumni-name">{{ p.name }}</span>

      <span class="alumni-meta">
        {% if p.degree %}{{ p.degree }}{% endif %}
        {% if p.year %} {{ p.year }}{% endif %}
        {% if p.years %} {{ p.years }}{% endif %}
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
