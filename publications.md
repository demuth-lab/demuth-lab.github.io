---
title: "Publications"
layout: default
---

<p class="lede">
For the most up-to-date list, see
<div class="scholar-links">
  <a href="{{ site.data.links.scholar }}"
     target="_blank"
     class="scholar-link">
    <i class="bi bi-mortarboard-fill"></i>
    Google Scholar
  </a>

  <a href="https://orcid.org/0000-0002-0471-3679"
     target="_blank"
     class="scholar-link">
    <i class="bi bi-link-45deg"></i>
    ORCID
  </a>
</div>
</p>

{% assign pubs = site.data.publications %}
{% assign topics = site.data.topics %}

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

<div class="pub-controls">

  <div class="pub-year-jump">
    <label for="yearJump"><strong>Jump to year:</strong></label>
    <select id="yearJump" onchange="if(this.value) location.hash=this.value;">
      <option value="">Select…</option>
      {% for y in years %}
        {% if y != "" %}
          <option value="#year-{{ y }}">{{ y }}</option>
        {% endif %}
      {% endfor %}
    </select>
  </div>

  <div class="pub-topic-jump">
    <label for="topicFilter"><strong>Filter by topic:</strong></label>
    <select id="topicFilter">
      <option value="">All topics</option>
      {% for kv in topics %}
        {% assign topic_id = kv[0] %}
        {% assign topic = kv[1] %}
        {% if topic and topic.label %}
          <option value="{{ topic_id }}">{{ topic.label }}</option>
        {% else %}
          <option value="{{ topic_id }}">{{ topic_id }}</option>
        {% endif %}
      {% endfor %}
    </select>
  </div>

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

  <li class="pub-item" data-tags="{% if p.tags %}{{ p.tags | join: ',' | downcase }}{% endif %}">

    <div class="pub-title">{{ p.title }}</div>

    <div class="pub-meta">
      {{ p.authors }} · <em>{{ p.venue }}</em> · {{ p.year }}
    </div>

    <div class="pub-links">
      {% assign view_href = nil %}

      {% if p.doi %}
        {% assign view_href = "https://doi.org/" | append: p.doi %}
      {% elsif p.url %}
        {% assign view_href = p.url %}
      {% elsif p.pdf %}
        {% assign view_href = p.pdf %}
      {% endif %}

      {% if view_href %}
        {% if p.type == "preprint" %}
          <a class="pub-link" href="{{ view_href }}" target="_blank" rel="noopener">View Preprint</a>
        {% else %}
          <a class="pub-link" href="{{ view_href }}" target="_blank" rel="noopener">View Article</a>
        {% endif %}
      {% endif %}

      {% if p.pdf and p.doi %}
        <a class="pub-link" href="{{ p.pdf }}" target="_blank" rel="noopener">Download PDF</a>
      {% endif %}

      {% if p.software and p.software.size > 0 %}
        {% for s in p.software %}
          <a class="software-link" href="{{ s.url }}" target="_blank" rel="noopener">{{ s.label }}</a>
        {% endfor %}
      {% endif %}
    </div>

  </li>

{% endfor %}
</ul>

<script>
(function () {
  const topicSel = document.getElementById("topicFilter");
  if (!topicSel) return;

  function applyFilter() {
    const chosen = (topicSel.value || "").trim().toLowerCase();

    const items = document.querySelectorAll(".pub-item");
    const yearHeaders = document.querySelectorAll(".pub-year");

    items.forEach((li) => {
      const tags = (li.getAttribute("data-tags") || "")
        .toLowerCase()
        .split(",")
        .map(s => s.trim())
        .filter(Boolean);

      const show = (!chosen) || tags.includes(chosen);
      li.style.display = show ? "" : "none";
    });

    yearHeaders.forEach((h2) => {
      const ul = h2.nextElementSibling;
      let anyVisible = false;

      if (ul && ul.classList.contains("pub-list")) {
        ul.querySelectorAll(".pub-item").forEach((li) => {
          if (li.style.display !== "none") anyVisible = true;
        });
      }

      h2.style.display = anyVisible ? "" : "none";
      if (ul && ul.classList.contains("pub-list")) {
        ul.style.display = anyVisible ? "" : "none";
      }
    });
  }

  topicSel.addEventListener("change", applyFilter);
})();
</script>
