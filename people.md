---
layout: page
title: People
permalink: /people/
---

## Principal Investigator

<div class="pi-wrap">
  <img class="pi-photo" src="/assets/img/people/Demuth_Headshot_2023.jpg" alt="Jeff Demuth">
  <div class="pi-text">
    <h3>Jeff Demuth</h3>
    <p><strong>Associate Professor, Department of Biology, University of Texas at Arlington</strong></p>

    <p>
      Jeff Demuth is an evolutionary geneticist studying how sex chromosomes and genome architecture shape behavioral responses to social conflict.
      His research integrates comparative genomics, regulatory evolution, and behavioral genetics in horned beetles and related systems.
    </p>

    <p class="pi-links">
      <a href="mailto:jpdemuth@uta.edu">jpdemuth@uta.edu</a>
      &nbsp;•&nbsp;
      <a href="YOUR_SCHOLAR_LINK">Google Scholar</a>
      &nbsp;•&nbsp;
      <a href="YOUR_ORCID_LINK">ORCID</a>
      &nbsp;•&nbsp;
      <a href="YOUR_CV_LINK">CV</a>
    </p>
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
