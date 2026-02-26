---
layout: page
title: People
permalink: /people/
---

## Principal Investigator

![Jeff Demuth](/assets/img/people/Demuth_Headshot_2023.jpg)

### Jeff Demuth  
**Associate Professor, Department of Biology, University of Texas at Arlington**

Jeff Demuth is an evolutionary geneticist studying how sex chromosomes and genome architecture shape behavioral responses to social conflict. His research integrates comparative genomics, regulatory evolution, and behavioral genetics in horned beetles and related systems. He received his PhD from Indiana University and joined UTA in 2006.

Email: jpdemuth@uta.edu  
[Google Scholar](#) | [ORCID](#) | [CV](#)

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
