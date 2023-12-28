
+++
date = "2013-11-13"
draft = false
title = "Node.js with AngularJS implementation of a KeePass2 browser"
slug = "node-js-with-angularjs-implementation-of-a-keepass2-browser"
tags = ['nodejs', 'angularjs', 'keepass', 'reader', 'browser', 'kdbx', 'treeview']
banner = ""
aliases = ['/node-js-with-angularjs-implementation-of-a-keepass2-browser/']
+++

A [Node.js](http://nodejs.org/) with [AngularJS](http://angularjs.org/) based implementation of a [KeePass2](http://www.keepass.info/) browser is [available](https://github.com/gesellix/keepass-node) at GitHub.

### What?
You should probably know about [KeePass](http://www.keepass.info/) as a tool to manage your passwords or other secrets in an encrypted file. Since the default tool to edit and view your passwords is based on .NET you might not be able to use your keys everytime you need them due to missing libraries or a wrong platform (Mono needs to be installed on Linux systems).

[KeePass-Node](https://github.com/gesellix/keepass-node) is based on the idea of [BrowsePass](http://bitbucket.org/namn/browsepass), which helps you to open a file from your current filesystem or from a URL by using only browser based libraries. To make BrowserPass more convenient, I didn't want to always upload a keepass file. I just wanted to enter a password to see my entries, so I searched for an improved solution. Long story short: I didn't find any, so I build it myself. [KeePass-Node](https://github.com/gesellix/keepass-node) was born.

### Usage
The installation is described in the [README.md](https://github.com/gesellix/keepass-node/blob/master/README.md) file. You'll only need a Node.js on your server, the rest should work out of the box. Some features are a bit rough on the edge and you still need to install a SSL  proxy in front of the keepass-node server in order to use the HTTPS protocol.

I didn't give it a try yet, but I'd like to use keepass-node as provider for browser plugins like [passifox](https://github.com/pfn/passifox/). I guess it should work, but if you already have some experience with such plugins, don't hesitate to [contact me](https://twitter.com/gesellix).

### Feedback
I would be glad about feedback, either via Twitter [@gesellix](https://twitter.com/gesellix) or by using the [issue tracker](https://github.com/gesellix/keepass-node/issues) at GitHub.
Thanks!


