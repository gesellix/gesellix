
+++
date = "2013-10-20"
draft = false
title = "Gradle Debian plugin"
slug = "gradle-debian-plugin"
tags = ['gradle', 'debian', 'plugin', 'java webapp']
banner = ""
aliases = ['/gradle-debian-plugin/']
+++

A new [Gradle](http://www.gradle.org/) plugin for creating [Debian](http://www.debian.org/) compatible packages (.deb) is available at [Bintray](https://bintray.com/gesellix/gradle-plugins/gradle-debian-plugin). It allows you to package any files through a convenient Gradle build script configuration into a Debian package compatible file. You may also include your MavenPublications (.jar or .war) by only referring to their publication names. To use the plugin you need some knowledge about the package structure and configuration scripts. The [Debian New Maintainers' Guide](http://www.debian.org/doc/manuals/maint-guide/index.en.html), chapters 4 and 5, will help a lot.

The current release v10 can be included in your Gradle buildscript dependencies. A minimal example is available in the readme file. The tests in the [GitHub repository](https://github.com/gesellix/gradle-debian-plugin) show you more complete examples on how to use the plugin to create a Java webapp package.

I'm still adding more tests to improve stability, but you may already start using it. Please give me some feedback or ask questions at the [GitHub issue tracker](https://github.com/gesellix/gradle-debian-plugin/issues)!

