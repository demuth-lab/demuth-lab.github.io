# Demuth Lab website (GitHub Pages)

This repo is a mobile-friendly Jekyll site designed for easy setup and maintenance.

## Quick start (GitHub Pages)
1. Create a new GitHub repo (e.g., `demuthlab-site`) and push this code.
2. In GitHub: **Settings → Pages**
   - Source: **GitHub Actions**
3. Your site will publish after the workflow runs.

## Edit content
- Home page: `index.md`
- People page (single page rendered from data): `_data/people.yml` + `assets/img/people/`
- Research themes: `research/*.md`
- Publications: `_data/publications.yml`
- News posts: `news/*.md`

## Publications workflow (Scholar-friendly)
Google Scholar doesn’t offer a stable public API, so the recommended workflow is:
1) Download the new publications as BibText (.bib) 
2) Append the new BibTeX file info `data/publications.bib`
3) Run the .github/workflows/publications workflow (will scrape for the dois)
4) Add any software links or other stuff using the 'data/publication_extras.yml' use the doi as keys
5) Add the doi for new [ubs to the data/topics.yml so it can be filtered correctly

Alternate method:

7) Either: Manually add the new stuff to _data/publications.yml
           OR Run `python3 scripts/bib2yaml.py` to regenerate `_data/publications.yml`
   

## Local preview
```bash
bundle install
bundle exec jekyll serve
```
Then open http://127.0.0.1:4000
