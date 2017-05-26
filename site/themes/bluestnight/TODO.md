## Widgets

- [ ] Add a blogroll / favorite links menu widget in the sidebar - .fi-link icon?
- [ ] Add search widget to sidebar - .fi-magnifying-glass icon
- [ ] Donate with Paypal widget? - .fi-paypal icon
- [x] Fix menu visibility issues
   - Menu is not visible on large screen if previously hidden (JS fix)
   - Menu is not visible on small screen if above happens (JS fix)
   - [x] Submenu does not expand after leaving small screen size (JS fix)
- [ ] [Google Analytics](https://gohugo.io/extras/analytics/)
- [ ] Custom ordering of widgets in the sidebar

## Archetypes
- [x] Add default archetype
- [x] Add archetype for `post`

## Posts

- [x] Add customizable and privacy-friendly comment system
- [x] Allow optionally overriding site page navigation setting
   - [ ] Optionally show only the next or previous nav, even if Hugo says the other exists
- [x] Optionally include a Table of Contents for the page

## Color scheme

- [x] Allow modification to certain base colors
- [x] Figure out how to get the nav elements to turn (accent color) on hover
- [x] Menu items that are also sub menus do not get marked active
   - [x] Items in sub menus are not marked active - limitation in Hugo?
- [x] (Optionally?) zebra stripe tables
- [x] Override the text selection color
- [x] .tag:active colors are not overridden
- [x] Headers need to underline in white
- [x] Sidebar widget headers should look like other headers, not turn accent color

## Templates

- [ ] Implement [blocks](https://gohugo.io/templates/blocks/)
- [x] Generate [pages for tags/categories](https://gohugo.io/templates/terms/) (also taxonomy lists on [this page](https://gohugo.io/templates/list/) and [this one](https://gohugo.io/taxonomies/displaying))
- ~~[ ] Custom [home page](https://gohugo.io/templates/homepage/)?~~
  - People should be able to use `_index.md` to modify their home page, even hiding the list
- [x] Templates for list pages containing `{{ .Content }}` for custom content ([Docs](https://gohugo.io/content/using-index-md/))

## Other
- [x] Reduce dependencies on JavaScript as much as possible
  - [x] Bonus: remove all dependencies on JavaScript so the theme is only HTML and CSS
     - [x] [CSS3 Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations/Using_CSS_animations) to show/hide menu
       - This is made harder by having Foundation as the CSS framework library because it determines how to organize the site based on screen size. I'd have to have a screen size rule matching the small screen detection for hiding the menu and showing the toggle, and another rule for doing the opposite on larger screens.
       - Perhaps I should also remove the dependency on Foundation, since it includes a bunch of styling I don't need anyways?
- [ ] Card-esque items in post list?
- [ ] Implement microdata based on [Schema.org](https://schema.org/docs/gs.html)
- [x] Use CSS3 [@page](https://developer.mozilla.org/en-US/docs/Web/CSS/@page) to modify the look for printing
- [ ] Use CSS3 [@viewport](https://developer.mozilla.org/en-US/docs/Web/CSS/@viewport) for small screens (Does Foundation already do this?)
- [ ] Use CSS3 [@supports](https://developer.mozilla.org/en-US/docs/Web/CSS/@supports) when necessary, e.g. for text select color
- ~~[ ] Add SASS/LESS support for people to generate their own style sheets instead of using generated <style> tags~~
  - Implemented Hugo-based CSS generation instead
