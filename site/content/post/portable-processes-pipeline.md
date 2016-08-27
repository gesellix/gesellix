
+++
date = "2015-11-06"
draft = true
title = "Portable Processes Pipeline"
slug = "portable-processes-pipeline"
tags = []
banner = ""
aliases = ['/portable-processes-pipeline/']
+++

You have certainly heard about deployment pipelines and Docker. If not, please [read this article](https://gesellix.net/have-fun-with-gradle-and-docker/), as it contains enough links to other relevant posts, articles, and examples.

#Status Quo
Most descriptions of a deployment pipeline describe several steps where application sources are compiled, tested, packaged, and ultimately distributed to a production server. Regardless of the actual language or environments of the application and the deployment pipeline, most of them have one thing in common: the pipeline steps get some artifacts (sources, packages, config) as input, do some stuff with them, and produce another artifact to be used in subsequent steps.

With Docker, the overall concept doesn't need to change. The advantages of Docker are easier setup of a build environment, a faster wrap up for throw-away test environments, and more stable packaging of an application including its runtime dependencies. Containerized builds also provide better encapsulation so that different builds on the same host don't interfere with each other. I have already described a [dockerized pipeline](https://github.com/gesellix/pipeline-with-gradle-and-docker) including example code, while another article (in German) describes a [server agnostic build environment](https://entwickler.de/?p=114302) for a node.js application.

An important aspect of passing artifacts around is the need for some storage or repository. Tools like Sonatype Nexus or the Docker Hub allow to use standardized mechanisms to share artifacts. When using CI servers like TeamCity you also have the option to share build artifacts between several build configurations, essentially defining a build chain.

Along with those concepts you also need to monitor disc space, consider retention strategies, and either buy storage or clean up old artifacts. If you're not so much into permanently buying additional storage, you might ask yourself how long artifacts need to be provided until they're candidates to be removed. The more radical question is: do you even need to keep an artifact for more than five minutes after a successful deployment? Do you really rollback to older versions?

What if it's ok not to keep the build artifacts around as soon as the production ready artifact has gone live? You might keep older versions available on mirrored production servers, just like a Blue/Green or A/B deployment allows by design. So, being prepared for a rollback doesn't imply to maintain a respository manager, huge storage or similar setup.

#(Trans-) Portable Processes
Allowing to remove intermediary build artifacts as soon as possible makes you think about variants of the standard pipeline. You might allow to perform several build steps on the sources, compiler artifacts, and packages not by passing the artifacts around, but by subsequently performing different actions on the same data -- in place.

With Docker you'll have a way to describe not only your data in volumes, but you can also describe actions similar to processes, no matter how complex an action is. The fact that every single tool of your toolbox is self contained and executable by a single command makes every action so simple.

Now what if for a commit in your code base you create a data volume and then run several processes on it. Every process reads and writes on that data volume, so that finally the deployable artifact just lies there. Each process can be regarded as a function, stateless and applyable on any data.

This isn't a shiny new idea: most Java developers are aware that modern build tools like Gradle perform all actions in a dedicated build directory. Whether the compiler, text replacements or packaging are necessary doesn't matter - everything is located in a single working tree. Why should other tools behave different?

Running tests or deploying an artifact on production servers has different effects and consequences, but from the point of an automated pipeline there's only a different command to be executed. The command can be successful or not, so that the pipeline will continue to run subsequent steps or stop at the failed one.

You can now argue that there needs to be separation of concerns, and that potential security issues enforce us to manually store artifacts in different locations. That way we can define access rules, audit traffic and actions, and we can completely lock down broken or insecure areas. Ok. Yes. But then you'll have to have multiple servers with separated parts of a pipeline performing the complete rollout for you, right? If not, you already have a single instance (the CI server) which might be a potential security issue.

Now I'm going to assume that it's ok to have a single CI server, because the actual deploy to a production server is somehow secured by other actions or constraints.



