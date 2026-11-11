# wilkens.io

Source for [wilkens.io](https://wilkens.io), built with [Hugo](https://gohugo.io) and deployed to GitHub Pages by `.github/workflows/pages.yml` on every push to `main`.

## Layout

- `content/blog/` and `content/research/`: one Markdown file per article. An article with images is a folder with `index.md` and the images beside it.
- `content/resume.md`, `layouts/_default/resume.html`: resume page.
- `data/projects.json`: projects shown on the home and projects pages.
- `layouts/`: templates. `static/css/site.css` is the compiled stylesheet carried over from the previous site; additions go in `static/css/extra.css`.
- `code/`: analysis scripts that back research articles.

## Publishing an article

Add a Markdown file with this front matter, then push to `main`.

```yaml
---
title: "Title"
date: "2026-11-11T12:00:00Z"
description: "One or two sentences shown on the list page and in link previews."
tags: ["Tag"]
---
```

## Preview locally

```sh
hugo server
```

Requires Hugo extended 0.147 or later.
