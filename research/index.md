---
title: "Research"
---
<div class="research-quotes">

  <blockquote class="quote-left">
    “Nothing in biology makes sense except in the light of evolution”
    <span class="quote-author">– T. Dobzhansky</span>
  </blockquote>

  <blockquote class="quote-right">
    “Nothing in evolution makes sense except in the light of population genetics”
    <span class="quote-author">– M. Lynch</span>
  </blockquote>

</div>

<p class="lede">We are trying to understand how life works and how it got that way from both evolutionary and functional perspectives.  We employ a variety of wet (molecular) and dry (computational) approaches to investigate the research topics below.</p>

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
