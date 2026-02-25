---
title: "Research"
---

<p class="lede">We use evolutionary genetics and genomics to understand how populations diverge and how gene and genome evolution shapes biological novelty.</p>

<div class="cards">
  {% for c in site.data.research_cards %}
    <a class="card" href="{{ c.url | relative_url }}">
      <h3>{{ c.title }}</h3>
      <p>{{ c.blurb }}</p>
    </a>
  {% endfor %}
</div>

<h2>Approach</h2>
<ul>
  <li>Experimental evolution and genetics in <em>Tribolium</em></li>
  <li>Population genomics and comparative genomics</li>
  <li>Quantitative genetics, gene expression, and computational methods</li>
</ul>
