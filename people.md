---
layout: page
title: People
permalink: /people/
---

## Principal Investigator

<div class="pi-wrap">

  <img class="pi-photo" src="/assets/img/people/Demuth_Headshot.jpg" alt="Jeff Demuth">

  <div class="pi-text">

    <h3 class="pi-name">Jeff Demuth</h3>

    <div class="pi-links">
      <a href="{{ site.data.links.scholar }}" target="_blank" rel="noopener">
        <i class="bi bi-mortarboard-fill"></i> Scholar
      </a>

      <a href="https://orcid.org/0000-0002-0471-3679" target="_blank" rel="noopener">
        <i class="bi bi-link-45deg"></i> ORCID
      </a>

      <a href="#" id="pi-email" data-user="jpdemuth" data-domain="uta.edu">
        <i class="bi bi-envelope-fill"></i> Email
      </a>
    </div>

    <p class="pi-title">
      Associate Professor, Department of Biology<br>
    </p>

    <p class="pi-admin">
      Associate Chair of Biology: 2014–2015; 2020–2025<br>
      Executive Member of the Division of Data Science: 2018-present
    </p>

    <p class="pi-degrees">
      Ph.D. Indiana University<br>
      M.S. Southeastern Louisiana University<br>
      B.S. Harding University
    </p>
    
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

<h3 class="alumni-heading">Postdocs</h3>
<ul class="alumni-list">
{% for person in alumni_people %}
{% if person.role == "postdoc" %}
  <li class="alumni-row">
    <div class="alumni-main">
      <span class="alumni-name"><strong>{{ person.name }}</strong></span>
      <span class="alumni-degree">{% if person.start_year and person.end_year %}{{ person.start_year }}–{{ person.end_year }}{% elsif person.end_year %}{{ person.end_year }}{% elsif person.start_year %}{{ person.start_year }}{% endif %}</span>
    </div>
  </li>
{% endif %}
{% endfor %}
</ul>

<h3 class="alumni-heading">PhD Students</h3>
<ul class="alumni-list">
{% for person in alumni_people %}
{% if person.role == "graduate" and person.degree == "PhD" %}
  <li class="alumni-row">
    <div class="alumni-main">
      <span class="alumni-name"><strong>{{ person.name }}</strong></span>
      <span class="alumni-degree">PhD{% if person.start_year and person.end_year %}, {{ person.start_year }}–{{ person.end_year }}{% elsif person.end_year %}, {{ person.end_year }}{% elsif person.start_year %}, {{ person.start_year }}{% endif %}</span>
    </div>
    {% if person.thesis_title %}
    <div class="alumni-thesis">PhD Dissertation: <em>{{ person.thesis_title }}</em></div>
    {% endif %}
  </li>
{% endif %}
{% endfor %}
</ul>

<h3 class="alumni-heading">M.S. Students</h3>
<ul class="alumni-list">
{% for person in alumni_people %}
{% if person.role == "graduate" and person.degree == "MS" %}
  <li class="alumni-row">
    <div class="alumni-main">
      <span class="alumni-name"><strong>{{ person.name }}</strong></span>
      <span class="alumni-degree">M.S.{% if person.start_year and person.end_year %}, {{ person.start_year }}–{{ person.end_year }}{% elsif person.end_year %}, {{ person.end_year }}{% elsif person.start_year %}, {{ person.start_year }}{% endif %}</span>
    </div>
    {% if person.thesis_title %}
    <div class="alumni-thesis">M.S. Thesis: <em>{{ person.thesis_title }}</em></div>
    {% else %}
    <div class="alumni-thesis">non-thesis</div>
    {% endif %}
  </li>
{% endif %}
{% endfor %}
</ul>

<h3 class="alumni-heading">Lab Managers</h3>
<ul class="alumni-list">
{% for person in alumni_people %}
{% if person.role == "lab_manager" %}
  <li class="alumni-row">
    <div class="alumni-main">
      <span class="alumni-name"><strong>{{ person.name }}</strong></span>
      <span class="alumni-degree">{{ person.degree }}{% if person.start_year and person.end_year %}, {{ person.start_year }}–{{ person.end_year }}{% elsif person.end_year %}, {{ person.end_year }}{% elsif person.start_year %}, {{ person.start_year }}{% endif %}</span>
    </div>
  </li>
{% endif %}
{% endfor %}
</ul>

<h3 class="alumni-heading">Undergraduate Research Assistants</h3>
<ul class="alumni-list">
{% for person in alumni_people %}
{% if person.role == "undergraduate" and person.degree == "BS" and person.thesis_title %}
  <li class="alumni-row">
    <div class="alumni-main">
      <span class="alumni-name"><strong>{{ person.name }}</strong></span>
      <span class="alumni-degree">B.S. Biology{% if person.end_year %}, {{ person.end_year }}{% elsif person.sort_year %}, {{ person.sort_year }}{% endif %}</span>
    </div>
    <div class="alumni-thesis">Honors Thesis: <em>{{ person.thesis_title }}</em></div>
  </li>
{% endif %}
{% endfor %}
</ul>

<p class="alumni-inline">
{% assign first = true %}
{% for person in alumni_people %}
  {% if person.role == "undergraduate" and person.degree == "BS" and person.thesis_title == nil %}

    {% unless first %} · {% endunless %}
    <span class="alumni-name"><strong>{{ person.name }}</strong></span>

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
