# Paperback

_Paperback_ is a minimalist theme for [Hugo](http://gohugo.io).

It focuses on improving reading experience with high contrast colors and no fancy effect.

It also uses [Highlight.js](https://highlightjs.org/) for the syntaxic coloration of code snippets.

## Installation

Please refer to the [Hugo documentation](http://gohugo.io/themes/installing/).

## Configuration

A few parameters can be adjusted in the site config:

```toml
[params]

# your name to display by the copyright sign
# default: undefined
AuthorName = "Firstname Lastname"

# tagline to show beneath homepage h1
# default: undefined
Tagline = "Hello, world!"

# number of posts to show on index
# default: 10
HomepagePosts = 3

# if set to true, social links will be displayed in the footer
# default: undefined
SocialLinks = true

# default: undefined
GithubUsername = "damiencaselli"

# default: undefined
TwitterUsername = "damiencaselli"
```

### Code highlighting

Both highlight theme and lib can be overridden. Just drop your build in the `static/js` directory, and the theme file in the `static/css` directory.  
Note that the theme has to be named `highlight.css`.
