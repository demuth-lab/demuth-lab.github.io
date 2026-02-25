---
title: "People"
---

<div class="section-title"><h2>Principal Investigator</h2></div>
<div class="grid-2">
  <div class="person">
    <img src="{{ site.data.people.pi.photo | relative_url }}" alt="{{ site.data.people.pi.name }}" loading="lazy" />
    <div class="name">{{ site.data.people.pi.name }}</div>
    <div class="role">{{ site.data.people.pi.role }}</div>
    <div class="interests">{{ site.data.people.pi.interests }}</div>
    <div class="links">
      <a href="mailto:{{ site.data.people.pi.email }}">Email</a>
      {% for l in site.data.people.pi.links %}
        <a target="_blank" rel="noopener" href="{{ l.url }}">{{ l.label }}</a>
      {% endfor %}
    </div>
  </div>
  <div class="card">
    <h3>Interested in joining?</h3>
    <p>We’re always excited to talk with curious, rigorous scientists who enjoy genetics, evolution, and/or computation.</p>
    <p><a class="button primary" href="{{ '/join/' | relative_url }}">How to apply</a></p>
  </div>
</div>

<div class="section-title"><h2>Graduate students</h2></div>
<div class="people-grid">
  {% for p in site.data.people.current_grads %}
    <div class="person">
      <img src="{{ p.photo | relative_url }}" alt="{{ p.name }}" loading="lazy" />
      <div class="name">{{ p.name }}</div>
      <div class="role">{{ p.role }}</div>
      {% if p.interests %}<div class="interests">{{ p.interests }}</div>{% endif %}
    </div>
  {% endfor %}
</div>

<div class="section-title"><h2>Undergraduate researchers</h2></div>
<div class="people-grid">
  {% for p in site.data.people.undergrads %}
    <div class="person">
      <img src="{{ p.photo | relative_url }}" alt="{{ p.name }}" loading="lazy" />
      <div class="name">{{ p.name }}</div>
      <div class="role">{{ p.role }}</div>
    </div>
  {% endfor %}
</div>

<div class="section-title"><h2>Alumni</h2></div>
<p class="muted">{{ site.data.people.alumni_note }}</p>
