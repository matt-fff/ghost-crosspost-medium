# medium-crosspost
[![DUB](https://img.shields.io/dub/l/vibe-d.svg)]()
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=typenil/ghost-crosspost-medium)](https://dependabot.com)
[![Build Status](https://travis-ci.org/typenil/ghost-crosspost-medium.svg?branch=master)](https://travis-ci.org/typenil/ghost-crosspost-medium)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f64916fe2fcbad4e9f7c/test_coverage)](https://codeclimate.com/github/typenil/ghost-crosspost-medium/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/f64916fe2fcbad4e9f7c/maintainability)](https://codeclimate.com/github/typenil/ghost-crosspost-medium/maintainability)


A Python script to crosspost articles to Medium.

Accompanies [this blog post](https://typenil.com/automatic-ghost-medium-cross-posting/), which goes into depth on crossposting between [Ghost](https://ghost.org/) and [Medium](https://medium.com/).

## Installation:
 
`pip install medium-crosspost`


## Basic Usage:

```
from medium_crosspost import MediumCrosspost

input_data = {
    "title": "Fantastic Article Name!",
    "canonicalUrl": "https://www.example.com/fantastic-article-name",
    "integrationToken": "super-secret-medium-integration-token",
    "content": "<html><head></head><body>Content is all about actual HTML-encoded article content.</body></html>",
    "tags": "can,be,a,list,or,comma,separated,string",
}

crosspost = MediumCrosspost(input_data)
result = crosspost.post()
```
