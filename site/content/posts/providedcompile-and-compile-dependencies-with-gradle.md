
+++
date = "2014-01-02"
draft = false
title = "ProvidedCompile and Compile Dependencies with Gradle"
slug = "providedcompile-and-compile-dependencies-with-gradle"
tags = ['gradle', 'transitive dependency', 'provided', 'compile', 'war plugin', 'validation-api']
banner = ""
aliases = ['/providedcompile-and-compile-dependencies-with-gradle/']
+++

When using the [Gradle](http://www.gradle.org/) [war plugin](http://www.gradle.org/docs/current/userguide/war_plugin.html) you're enabled to declare `providedCompile` dependencies to tell the compiler to include those dependencies in the compile classpath, but to not make Gradle include them in the packaged .war artifact. Your build.gradle script might look like this, e.g. for a webapp using GWT:
```
apply plugin: 'war'

dependencies {
  ...
  providedCompile 'com.google.gwt:gwt-user:2.5.1'
  ...
}
```

The dependency shown in the example has some own dependencies, which can be shown by using the `:dependencies` task. You should get a dependency tree like the snippet below:
```
...
providedCompile - Additional compile classpath for libraries that should not be part of the WAR archive.
\--- com.google.gwt:gwt-user:2.5.1
     +--- javax.validation:validation-api:1.0.0.GA
     \--- org.json:json:20090211
...
```

You might now want to have some Validation in your application, so you'd like to use the `validation-api` as already provided through the transitive dependency of `gwt-user`. Since Gradle won't package provided dependencies, you might declare the `validation-api` with a compile scope, so that your build script looks like follows:
```
apply plugin: 'war'

dependencies {
  ...
  compile 'javax.validation:validation-api:1.0.0.GA'
  providedCompile 'com.google.gwt:gwt-user:2.5.1'
  ...
}
```

Well, when now calling the Gradle build task, and deploying the created .war artifact you'll notice that the validation-api hasn't been packaged. An explanation can be found at a Gradle [forum thread](http://forums.gradle.org/gradle/topics/war_plugin_not_including_certain_compile_dependencies_in_war) telling you to disable transitive dependencies for cases like shown above. The solution for the example above would look like this:
```
apply plugin: 'war'

dependencies {
  ...
  compile 'javax.validation:validation-api:1.0.0.GA'
  providedCompile ('com.google.gwt:gwt-user:2.5.1') {
    transitive = false
  }
  ...
}
```
Please read the linked forum thread completely for details!


