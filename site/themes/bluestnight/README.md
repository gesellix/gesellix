# BluestNight
A dark theme with blue accents for Hugo. Provides multiple configuration options and overrides.

This theme is a complete recreation of my previous theming attempt [Darkroad](https://github.com/Shadow53/Darkroad) based on [Mainroad by Vimux](https://github.com/vimux/mainroad). The theme is similar only in basic structure and has been recreated from scratch.

### Example sites
See the theme in action with its custom color scheme [here](https://mnbryant.com) or with an override [here](https://shadow53.com)

### Features

You can find more details on certain features by scrolling down past this list

- [Site header with tagline](#site-headertagline)
- Responsive design using [CSS flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Using_CSS_flexible_boxes)
- [Configurable color scheme](#custom-colors)
- [Custom site wallpaper](#custom-wallpaper)
- Custom CSS that cleans the page up for printing *only* the page content (try visiting one of the example pages and viewing print preview)
- [Custom shortcodes](#shortcodes) that I find useful
- [Multiple sidebar widgets](#sidebar-widgets), including:
  - Categories list
  - Recent posts list
  - Post tags list (sorted by most common)
  - Patreon banner
- Optional [authorbox](#authorbox) on post pages
- `_index.md` support for all list pages, including custom content and hiding the list
- Pagination
- [Custom section landing pages](#custom-section-landing-pages)
- Dynamic site menu that works on desktop and mobile alike - supports seemingly infinite nesting (might look bad on mobile, though)
- Comments system based on [Hashover](http://tildehash.com/?page=hashover) (requires PHP on the hosting server)
  - Comments can be enabled/disabled on a per-page basis as well as in the site config
- Dynamic taxonomy pages that look good on all screen sizes
- Custom "Error 404" page
- Custom robots.txt that prevents taxonomy pages from being indexed (e.g. /tags/my_tag)
- Check out the [TODO list](https://github.com/Shadow53/BluestNight)

### Template `config.toml`

```toml
languageCode = "en-us"
title = "My Website"
baseurl = "https://example.com/"
theme = "BluestNight"
enableRobotsTXT = true # Use custom robots.txt
PygmentsCodeFences = true
PygmentsStyle = "monokai" # Use "igor" for light backgrounds

[Params]
    tagline = "An example tagline for my Hugo site" # Subtitle of your site
    description = "Here is a description of my site that will appear in search engine results - W00t!" # Description of your site
    authorbox = true
    author = "Some Guy" # Name must exist in an entry in /data/members
    post_navigation = false
    # HashOver requires PHP running on the server
    # and cannot be hosted on a different domain
    hashover = false

# Custom background for the site
[Params.background]
    src = "/path/to/background.png"
    fit_width = true
    tile = false

[Params.widgets]
    recent_articles = true # Enable "Recent arcticles" widget
    categories = true # Enable "Categories" widget
    tags = true # Enable "Tags" widget
    patreon = "https://patreon.com/shadow53" # Enable "Patreon" widget
    tags_counter = true # Enable tag count on tag widgets

# These are the default colors used in the theme
# Change them to whatever you'd like
[Params.color]
    page_background_color = "#000000"
    main_background_color = "#050505"
    alt_background_color = "#252525"
    body_text = "#e2e2e2"
    alt_body_text = "#e2e2e2"
    accent_color = "#2c8cef"
    header_text = "#e2e2e2"

# This is required for CSS to work
[outputs]
    home = ["HTML", "CSS"]

```

### Site Header/Tagline

At the top of each page is a site header containing the name of the website in
large letters and, if a tagline is specified, the tagline in smaller letters
underneath the site's name. To add a tagline, add this line under `[Params]` in
`config.toml` (modify as necessary if you use YAML or JSON):

```toml
tagline = "This is my site's tagline" # Subtitle of your site
```

### Custom colors

Change any or all of the page colors by including this in your `config.toml` file:

```toml
[Params.color]
    # Background of page behind site container, where background image goes
    page_background_color = "#000000"
    # Background of site container
    main_background_color = "#050505"
    # Alternate background of site container, used on inactive buttons,
    # alternatings table rows, and <code> and <pre> elements (code fields)
    alt_background_color = "#252525"
    # The text color to correspond with main_background_color
    body_text = "#e2e2e2"
    # The text color to correspond with alt_background_color
    alt_body_text = "#e2e2e2"
    # Accent color, used for active buttons, links, and the site header
    accent_color = "#2c8cef"
    # A text color to correspond with using accent_color as a background color
    header_text = "#e2e2e2"
```

This requires also adding `CSS` as an output type for the home page, e.g.:

```toml
[outputs]
    home = ["HTML", "CSS"]
```

Also, if you plan on displaying code on your site, add these two lines as root
options in `config.toml`:

```toml
PygmentsCodeFences = true
PygmentsStyle = "monokai"
```

Change the `PygmentsStyle` option to your favorite color scheme that goes well
your site's theme. `monokai` is good for dark themes and I like `igor` for light
themes.

### Custom wallpaper

Add the following to your `config.toml` to have a site background image:
If you do not tile the image, it gets anchored in the top-left corner of the window

```toml
[Params.background]
    # Path or link to the image
    src = "/images/background.jpg"
    # Shrink image to fit the full width in the window?
    fit_width = true
    # Tile the image?
    tile = false
```

### Sidebar widgets

```toml
[Params.widgets]
    # Show the ten most recent posts under /post/
    recent_articles = true
    # Show the top 5 categories in use on your site
    categories = true
    # Show the tags used on your site, ordered by most common
    tags = true
    # Include a parenthetical count of how often a tag has been used
    tags_counter = false
    # Show a Patreon banner in the sidebar linking to the URL below
    # Note: Since this is originally a dark theme, the banner used is white.
    # Eventually I will get around to making it configurable
    patreon = "https://patreon.com/shadow53"
```

### Authorbox

The Authorbox provides attribution to the author of a given post. To enable
authorboxes sitewide, include the line `authorbox = true` under `[Params]`
in `config.toml`.

You can also override the sitewide setting by setting `authorbox` in the front
matter of a piece of content.

To display a person's information in the authorbox, you need two more things.
First, a data file under `/data/members/` that has the following information:

```yaml
# This example uses YAML
Name     : "Michael Bryant"
Img      : "/path/to/picture/of/michael.jpg"
Position : "Awesome Theme Designer"
Bio      : |
  I'm Michael
```

Then, on the page you are attributing to this person, set the `author` variable
to the same value as `Name` in the data file - in this case,
`author = "Michael Bryant"`. As long as authorboxes are enabled for the page,
Michael's authorbox will be displayed at the bottom of the page.

### Custom Section Landing Pages

Rather than have Hugo generate a page of nothing but the content under a section,
maybe you'd like to introduce the content with a paragraph or two first. If you
place a `_index.md` file with the desired content in the root of the section folder,
BluestNight will place that text before the content list.

Bonus! If you want to hide the list and show only your custom content, just add
a line setting `hide_list` to `true` in the front matter of `_index.md`.

### Shortcodes

#### Member Boxes

The memberbox is equivalent to the authorbox, except that memberboxes can be
displayed anywhere in a piece of content using the `{{< member "Member Name" >}}`
shortcode. Replace `Member Name` with the name of the member as found in the
`Name` attribute of the data file in `/data/members/`. See [Authorbox](#authorbox)
for more on the data file.

##### Example:

```markdown
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque convallis sollicitudin arcu sed volutpat. Suspendisse ante erat, elementum eget orci a, consectetur condimentum est. Sed leo ipsum, laoreet eu rhoncus id, posuere ut sem. Pellentesque blandit, tortor sit amet lobortis tristique, sem felis pellentesque orci, vel interdum lacus magna et est. In fringilla facilisis ultrices. Maecenas at bibendum tellus. Vivamus imperdiet volutpat lacus, a tempor enim rutrum at.

{{< member "Joe Smith" >}}

Sed tristique ex eros. Donec vestibulum nunc sed mattis efficitur. Mauris mollis libero quis tellus interdum, id venenatis dolor gravida. Praesent dignissim tempor blandit. Duis ut nisi eget arcu molestie dapibus. Cras viverra magna id tincidunt ultrices. Nam id cursus diam, in ultricies sem. Ut convallis eget metus non feugiat. Integer elementum consequat risus vitae lobortis. Curabitur dapibus, lectus nec vulputate laoreet, leo elit gravida odio, ac dapibus nisl ex vel justo. Maecenas ornare lobortis ante nec blandit.
```

#### Handwriting styles

The theme comes with a handful of 100% free handwriting fonts from [Font Squirrel](https://www.fontsquirrel.com/). You can choose between them using the `{{% handwriting %}}` shortcode. These are the currently available fonts:

- `"allura"`
- `"calligraffiti"`
- `"dancing-script"`
- `"daniel"`
- `"euphoria-script"`
- `"journal"`
- `"kingthings-wrote"`
- `"note-this"`
- `"vag-handwritten"`

##### Example:

```
{{% handwriting "calligraffiti" %}}
This is some text that will render using the "calligraffiti" font.
{{% /handwriting %}}
```
