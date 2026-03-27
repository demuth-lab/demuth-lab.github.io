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

<p class="lede">We are trying to understand how life works using the tools of evolutionary and functional genetics and genomics.  Currently, there are three broad areas of active research in the lab.  All three areas employ a variety of molecular and computational approaches.
</p>

<div class="cards">
  {% assign research_pages = site.research | sort: "order" %}
  {% for p in research_pages %}
    <a class="card card--image"
       href="{{ p.url | relative_url }}"
       style="--card-img:url('{{ p.card_image | default: p.hero_image | relative_url }}')">
       
      <h3>{{ p.card_title | default: p.title }}</h3>

    </a>
  {% endfor %}
</div>

<h2>Approach</h2>
<ul>
  <li>Experimental evolution and genetics in <em>Tribolium</em></li>
  <li>Population genomics and comparative genomics</li>
  <li>Quantitative genetics, gene expression, and computational methods</li>
</ul>
