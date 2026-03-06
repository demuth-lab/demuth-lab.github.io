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

{% assign current_people = site.data.people | where: "status", "current" %}
{% assign alumni_people = site.data.people | where: "status", "alumni" | sort: "sort_year" | reverse %}

---

## Graduate Students

<div class="people-grid">
{% for person in current_people %}
{% if person.role == "graduate" %}
  <div class="person-card">
    <img src="{{ person.photo }}" alt="{{ person.name }}">
    <h4>{{ person.name }}</h4>
    {% if person.bio %}<p>{{ person.bio }}</p>{% endif %}
  </div>
{% endif %}
{% endfor %}
</div>

---

## Undergraduate Research Assistants

<div class="people-grid">
{% for person in current_people %}
{% if person.role == "undergraduate" %}
  <div class="person-card">
    <img src="{{ person.photo }}" alt="{{ person.name }}">
    <h4>{{ person.name }}</h4>
    {% if person.bio %}<p>{{ person.bio }}</p>{% endif %}
  </div>
{% endif %}
{% endfor %}
</div>

---

## Lab Alumni

<h3>Postdocs</h3>
<ul class="alumni-list">
{% for person in alumni_people %}
{% if person.role == "postdoc" %}
  <li class="alumni-row">
    <div class="alumni-main">
      <span class="alumni-name">{{ person.name }}</span>
      <span class="alumni-degree">{{ person.degree }}{% if person.start_year and person.end_year %}, {{ person.start_year }}–{{ person.end_year }}{% elsif person.end_year %}, {{ person.end_year }}{% elsif person.start_year %}, {{ person.start_year }}{% endif %}</span>
    </div>
  </li>
{% endif %}
{% endfor %}
</ul>

<h3>PhD Alumni</h3>
<ul class="alumni-list">
{% for person in alumni_people %}
{% if person.role == "graduate" and person.degree == "PhD" %}
  <li class="alumni-row">
    <div class="alumni-main">
      <span class="alumni-name">{{ person.name }}</span>
      <span class="alumni-degree">PhD{% if person.start_year and person.end_year %}, {{ person.start_year }}–{{ person.end_year }}{% elsif person.end_year %}, {{ person.end_year }}{% elsif person.start_year %}, {{ person.start_year }}{% endif %}</span>
    </div>
    {% if person.thesis_title %}
    <div class="alumni-thesis"><strong>PhD Dissertation:</strong> <em>{{ person.thesis_title }}</em></div>
    {% endif %}
  </li>
{% endif %}
{% endfor %}
</ul>

<h3>M.S. Alumni</h3>
<ul class="alumni-list">
{% for person in alumni_people %}
{% if person.role == "graduate" and person.degree == "MS" %}
  <li class="alumni-row">
    <div class="alumni-main">
      <span class="alumni-name">{{ person.name }}</span>
      <span class="alumni-degree">M.S.{% if person.start_year and person.end_year %}, {{ person.start_year }}–{{ person.end_year }}{% elsif person.end_year %}, {{ person.end_year }}{% elsif person.start_year %}, {{ person.start_year }}{% endif %}</span>
    </div>
    {% if person.thesis_title %}
    <div class="alumni-thesis"><strong>M.S. Thesis:</strong> <em>{{ person.thesis_title }}</em></div>
    {% else %}
    <div class="alumni-thesis">non-thesis</div>
    {% endif %}
  </li>
{% endif %}
{% endfor %}
</ul>

<h3>Lab Managers</h3>
<ul class="alumni-list">
{% for person in alumni_people %}
{% if person.role == "lab_manager" %}
  <li class="alumni-row">
    <div class="alumni-main">
      <span class="alumni-name">{{ person.name }}</span>
      <span class="alumni-degree">{{ person.degree }}{% if person.start_year and person.end_year %}, {{ person.start_year }}–{{ person.end_year }}{% elsif person.end_year %}, {{ person.end_year }}{% elsif person.start_year %}, {{ person.start_year }}{% endif %}</span>
    </div>
  </li>
{% endif %}
{% endfor %}
</ul>

<h3>Undergraduate Honors Theses</h3>
<ul class="alumni-list">
{% for person in alumni_people %}
{% if person.role == "undergraduate" and person.degree == "BS" and person.thesis_title %}
  <li class="alumni-row">
    <div class="alumni-main">
      <span class="alumni-name">{{ person.name }}</span>
      <span class="alumni-degree">B.S. Biology{% if person.end_year %}, {{ person.end_year }}{% elsif person.sort_year %}, {{ person.sort_year }}{% endif %}</span>
    </div>
    <div class="alumni-thesis"><strong>Honors Thesis:</strong> <em>{{ person.thesis_title }}</em></div>
  </li>
{% endif %}
{% endfor %}
</ul>

<h3>Undergraduate Research Assistants</h3>

<p class="alumni-inline">
{% assign first = true %}
{% for person in alumni_people %}
  {% if person.role == "undergraduate" and person.degree == "BS" and person.thesis_title == nil %}

    {% unless first %} · {% endunless %}
    {{ person.name }}

    {% assign first = false %}
  {% endif %}
{% endfor %}
</p>

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
