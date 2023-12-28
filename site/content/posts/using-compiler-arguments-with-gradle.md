
+++
date = "2013-12-16"
draft = false
title = "Using Compiler Arguments with Gradle"
slug = "using-compiler-arguments-with-gradle"
tags = ['gradle', 'compiler arguments', 'compilerArgs']
banner = ""
aliases = ['/using-compiler-arguments-with-gradle/']
+++

Just in case you're searching for a way to use multiple compiler arguments in your [Gradle](http://www.gradle.org/) builds, have a look at this snippet:

	subprojects {
        tasks.withType(JavaCompile) {
        	options.compilerArgs << "-Xlint:unchecked" << "-Xlint:deprecation"
        }
    }

I took the example from [stackoverflow](http://stackoverflow.com/questions/18689365/how-to-add-xlintunchecked-to-my-android-gradle-based-project), but you can find details at the Gradle DSL for the [JavaCompile](http://www.gradle.org/docs/current/dsl/org.gradle.api.tasks.compile.JavaCompile.html#org.gradle.api.tasks.compile.JavaCompile:options) class.


