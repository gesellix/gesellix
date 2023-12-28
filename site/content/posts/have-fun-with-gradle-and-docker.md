
+++
date = "2014-07-27"
draft = false
title = "Deploying with Gradle and Docker: have fun"
slug = "have-fun-with-gradle-and-docker"
tags = ['gradle', 'docker', 'continuous deployment', 'devops']
banner = ""
aliases = ['/have-fun-with-gradle-and-docker/']
+++

Deploying products to production is a quite individual process for every application. Building deployment pipelines has already been described on a high level of abstraction, e.g. by the ThoughtWorks guys Jez Humble, Dan North and Chris Read in their paper [The Deployment Production Line](http://dl.acm.org/citation.cfm?id=1155519), not to forget the more general theme about [Continuous Delivery](http://www.thoughtworks.com/de/continuous-delivery) being described in its own book by Jez Humble and David Farley.

You might search for tools implementing the according patterns, and you'll find some like [ThoughtWorks Go](http://www.go.cd/) (it's free!) or Continuous Integration tools like [TeamCity](http://www.jetbrains.com/teamcity/) or [Jenkins](http://jenkins-ci.org/) enabling you to describe build chains with several build steps.

Some aspects of your build pipeline aren't implemented in such tools, though, because they cannot model your individual needs. So you end up writing shell scripts or other "low level" descriptions of your deployment details. That's no problem per se, but this is where you also have to think about how to maintain your deployment and infrastructure code.

## fill the gap

[Infrastructure as code](http://www.ibm.com/developerworks/library/a-devops2/) is one aspect maintaining and stabilizing your infrastructure - you certainly know [Puppet](http://puppetlabs.com/) or [Chef](http://www.getchef.com/) addressing your needs, and there's a massive increase of similar tools like [SaltStack](http://www.saltstack.com/) and [Ansible](http://www.ansible.com/) that can be used on top or instead of the established tools.

Since you cannot draw a clear line where your infratructure ends and where your application begins, you probably have some shell scripts quite near your application code base. Such scripts or build tools with their plugins handle tasks like running tests, packaging of libraries and static resources, publishing artifacts to repositories, downloading them to test and production servers, stopping and redeploying your application or other services and probably configuring a router to make new requests reach the new release.

Over time you add some more services participating your deployments, and you'll end up with some more shell scripts, some more plugins, some more configuration, some more aspects to keep in mind. But this is probably not always fun.

You need to orchestrate. This can be fun, but it's also a job to be done.

## have fun

How would you have more fun maintaining your deployments? There's no general answer. Let's face it, it's your individual deployment. But reading articles or books and exchanging ideas can improve your and other solutions, provide new aspects or even tools.

We would like to share our experience about deploying a non-trivial [Spring Boot](http://projects.spring.io/spring-boot/) application including an [AngularJS](https://angularjs.org/) frontend, talking with several other services and being implemented with a growing DevOps culture in mind.

Our build tool of choice is [Gradle](http://www.gradle.org/), we use TeamCity as CI server and Gradle scripts to orchestrate test infrastructure and deployments, while our application is packaged in [Docker](https://www.docker.com/) images. We can say that "it just works"&trade; and it definitely makes fun.

In order to give you an idea how such a setup works for us, we've started a little series on our employer's [IT blog](http://blog-it.hypoport.de/) at [Hypoport](http://www.hypoport.de/). Please check back from time to time to read about details, but also to use the chance to give feedback. Feel free to ask questions on unclear subjects and suggest other topics, so we can write about according details. You can use the comments section on the IT blog or get in contact via Twitter [@gesellix](https://twitter.com/gesellix).

So, go ahead to the first article about our [Continuous Deployment Pipeline with Gradle and Docker](http://blog-it.hypoport.de/2014/07/25/a-continuous-deployment-pipeline-with-gradle-and-docker/) with an overview of our setup and stay tuned for updates!


