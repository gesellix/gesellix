
+++
date = "2014-07-03"
draft = false
title = "Gradle-Docker-Plugin and Docker-Client available"
slug = "gradle-docker-plugin-and-docker-client-available"
tags = ['gradle', 'plugin', 'docker', 'client']
banner = ""
aliases = ['/gradle-docker-plugin-and-docker-client-available/']
+++

In line with [our deployment pipeline](http://gesellix.github.io/gradle-summit-2014/?full#deployment-pipeline) written in Gradle and using Docker, we currently use Groovy's process execution methods to talk with a command line Docker client.

That way we make ourselves dependent to an installed Docker client on our CI servers. Since we don't like to provide a bunch of specific CI servers, I started to implement a HTTP client for Docker, written in Groovy. The reason not to use existing Java implementations of such a Docker client was simply timing: some months ago the now completely rewritten [Java Docker API Client](https://github.com/docker-java/docker-java) wasn't so well maintained than today... and, well, I like to play with new tools and wanted to explore the Docker remote API for myself.

Using a Java API would be one possible solution to rewrite our Gradle scripts, but in order to implement a higher level interface on top of the HTTP wrapper I wanted to use Gradle plugin mechanisms and a simple task configuration.

So here they are: the inevitable duo of a [Docker-Client](https://github.com/gesellix-docker/docker-client) written in Groovy and a [Gradle-Docker-Plugin](https://github.com/gesellix-docker/gradle-docker-plugin) - along with a small Gradle [example project](https://github.com/gesellix-docker/gradle-docker-plugin-example).

Please have a look at the projects, give them a try and if you find any missing feature or bug, please create an issue at one of the projects linked above! I would also be glad about feedback, either via Twitter [@gesellix](https://twitter.com/gesellix) or by mail (tobias @ gesellix.de). Thank you!


