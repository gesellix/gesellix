
+++
date = "2013-10-27"
draft = false
title = "Using Coveralls in your Gradle build"
slug = "using-coveralls-in-your-gradle-build"
tags = ['gradle', 'plugin', 'coveralls', 'coverage', 'build', 'travis-ci']
banner = ""
aliases = ['/using-coveralls-in-your-gradle-build/']
+++

Recently I stumbled over a tool [Coveralls](https://coveralls.io/). It helps monitoring your test coverage. You can integrate it e.g. with your [Travis-CI](https://travis-ci.org/) builds by using a plugin for your favorite build tool. Needless to say that they also provide Travis-CI similar badge to show off your current test coverage near your current build status in your README file at [GitHub](https://github.com/).

Their docs sadly aren't very focused on Java tools like Maven or Gradle, so you have to find a working plugin on your own (or code a new one by using the Coveralls API). I tried the [coveralls-gradle-plugin](https://github.com/kt3k/coveralls-gradle-plugin) for my [gradle-debian-plugin](https://github.com/gesellix/gradle-debian-plugin) and it works like a charm! Just have a look at the [list of results](https://coveralls.io/r/gesellix/gradle-debian-plugin) - showing some potential to improve test coverage ;-)

