
+++
date = "2015-07-11"
draft = false
title = "On Library Dependencies and API Evolution"
slug = "choosing-a-library"
tags = ['gradle', 'docker', 'client', 'library', 'dependency', 'api', 'evolution', 'maven']
banner = ""
aliases = ['/choosing-a-library/']
+++

As maintainer for publicly available libraries one sometimes has to answer feature requests or handle feedback about missing features of the library. How does one prepare for different requirements? I'd like to tell you how and why I opted to implement yet another docker http client on my own and I'll also try to explain where I see its benefits and disadvantages.

## not invented here syndrome?

You have probably seen several [Docker remote api client libraries](https://docs.docker.com/reference/api/remote_api_client_libraries/) for different environments or programming languages. During the development of the [Gradle Docker plugin](https://github.com/gesellix/gradle-docker-plugin) I had to choose how to communicate with the Docker remote api. The [Java Docker API Client](https://github.com/docker-java/docker-java) aka docker-java already existed, but wasn't mature enough to simply use it for my needs. Other alternatives have been rare, so I decided to implement the remote api client on my own.

Using Groovy, it was quite convenient to communicate with the RESTful remote api. Implementing an own docker library helped to have fast development cycles because I didn't have to wait for another library to add necessary features. I also relied on Groovy's dynamic typing, so that I didn't need to keep up with remote api changes.

The best example where the dynamic typing has been helpful is the `create container` endpoint with its port mappings and volume binds being configured in a JSON encoded request body. Groovy allowed me to implement such a payload as simple key/value map.

## where reality kicks in

Due to the low level nature of the remote api, including [hijacking hacks](https://docs.docker.com/reference/api/docker_remote_api_v1.19/#3-2-hijacking) on `/attach`, the Apache Http Client reached some limits. Even the Groovy HttpBuilder project hasn't been very active during the last year, so that it [wasn't possible](https://github.com/jgritman/httpbuilder/issues/21) to use it with a more recent Http Client 4.3.x release. Similar dependency issues hit the docker-java library, e.g. [dependency conflicts](https://github.com/docker-java/docker-java/issues/64) of the JAX-RS library when used in certain environments.

Regarding the docker-java library, which provides a strongly typed and fluent api, we can observe a high amount of smaller maintenance tasks when new options are added to the Docker remote api. There are many pull requests which don't add any logic, but only extend the api to pass parameters through to the actual http layer. There's nothing wrong with that, but it's another approach with advantages and disadvantages.

So which library would you choose? I only mentioned two libraries, but as you might guess there are other libraries available and they all have their useful niche. Nothing comes without tradeoffs, though.

## adjust and adapt

Instead of trying to work around problems I tried to remove them. I searched for alternatives of the Apache Http Client so that I could easily solve some of my issues with chunked responses or hijacked sockets. I didn't find any alternatives, but why? I didn't expect to be the first looking for a more flexible http client. After a while I gave up on finding a better http client library. It seemed like the Apache Http Client was a very good choice. Nevertheless I had problems with it.

Still trying to remove problems, I considered implementing an http client on my own. Sounds stupid: there's this little developer sitting at his desk, criticising a well-known and mature Apache library, but nonetheless thinking about implementing something better.

I didn't need many features like sophisticated connection pooling, and only wanted to perform simple requests with better control on response handling. The `HttpURLConnection` doesn't provide a very convenient api, but it's the highest level abstraction in the JDK which knows enough about HTTP without depending any external dependencies.

Reading about existing JDK features I learned about concepts like protocol handlers as combination of the URLConnection and a [URLStreamHandler](http://docs.oracle.com/javase/7/docs/api/java/net/URLStreamHandler.html), and [ContentHandlers](http://docs.oracle.com/javase/7/docs/api/java/net/ContentHandler.html). Such concepts helped me adding HTTP over unix socket support and reading Docker's [raw streams](https://docs.docker.com/reference/api/docker_remote_api_v1.19/#attach-to-a-container). Even HTTPS support was less complex than expected.

The current [LowLevelDockerClient](https://github.com/gesellix/docker-client/blob/master/src/main/groovy/de/gesellix/docker/client/LowLevelDockerClient.groovy) is probably not the most beautiful piece of code, but it does its job and I didn't have any major issues with it yet. As usual, less code is good code and other mature http client libraries are probably _just too big_ for my use case.

## with less dependencies flexibility is improved

There's nothing special with yet another http client, and I guess I have some luck that the docker-client library isn't very popular compared to the docker-java library: with more users the potential to stumble on missing feature is increased a lot. Nevertheless I'm very satisfied with the result, because it's the minimal amount of code necessary to talk to the Docker daemon, it's less blown than a more generic library like JAX-RS, and it's very focused on a lean workflow when it comes to modifying or extending the library.

This is not about bashing other bigger libraries. This is not about judgement which library is the better one. This is about use cases and certain contexts of other developers searching for a way to talk to an http enabled service.

## users and their use cases

I see at least two groups of developers: one group likes to be led by an explicit api, which has the advantage that some low level aspects can be hidden from them. Such an api helps recognising breaking changes at compile time. As mentioned above, the advantages can also be disadvantages when it comes to maintainability: Docker is a moving target (and it moves fast), so a library talking to Docker needs to keep up with the pace, otherwise it won't be able to satisfy its users' needs. Yet, this first group of developers probably doesn't want to move so fast, which makes a less flexible library even more attractive to them.

Another group of developers likes it the bleeding edge way of life. They are the ones who try release candidates, read changelogs and the remote api documentation very carefully before going to bed, and don't want a library to stand in their way.

One much anticipated Docker feature to mark containers with labels (instead of only container names) was only a simple new property in the `create container` request body... at least from the remote api client's point of view. How many lines of code needed to be changed in docker-java and docker-client, respectively? Well, in docker-client, I didn't need to change any line. _No single line_. In docker-java, they needed to add [about 34 lines](https://github.com/docker-java/docker-java/commit/2d3174528c59d2ebe2255fc3596fc1d1adac2cdb) of code, which ultimately only changes a single field.

Again, this is not about a battle of libraries! This is about different design decisions and their effects on maintenance and user's code. The main difference to me lies in the way a library allows a user to use new features.

One library passes data from the user to the actual endpoint. The other library needs a new release before a user can send enhanced data to the endpoint. The first library doesn't care about the data, the second library doesn't even allow one to bypass its api. The first library doesn't check or validate the data, while the second library removes a huge amount of potential errors just by design.

You see: there's no simple good or bad. There's only a user with a use case and some constraints or expectations. If you expect a library to protect yourself from fundamental errors in your code, you'll often have to accept foreign contraints. If you only need a simple library to pass your data to another system and only handle low level stuff for you, then you should be prepared that some aspects need to be solved on your side.

For me, simplicity is very important. Libraries might be popular, mature, and feature rich. But they need to stay simple. Otherwise complexity and restrictions can creep into the consumers' code which also increases the risk of breaking changes. Too much simplicity can lead to niche existence, which can be optimal for a small use case, but can minimize innovation due to less challenges from different consumers.

## summary

I wouldn't say that one single library for a use case is enough. It's good to have different solutions and the chance to evaluate each. I only mentioned two Docker client libraries explicitly, but you can find at least four different ones being actively developed. The same applies to [Maven Docker plugins](https://github.com/rhuss/shootout-docker-maven) or Gradle Docker plugins. Since I mentioned my own [Gradle Docker plugin](https://github.com/gesellix/gradle-docker-plugin) above, I would also like you to have a look at [another nice plugin](https://github.com/bmuschko/gradle-docker-plugin). Fun fact: it internally uses the docker-java library.

Comparing similar libraries or frameworks should be made easier, though. It's very hard to find the best solution in similar libraries, when every library seems to have all necessary features. Usually, the most popular choice won't be too wrong. But is it the _best_ solution for your own needs?

In my experience, minimizing dependencies was a good choice, even for the tradeoff of implementing something from scratch. I also prefer to keep an api as less restrictive as possible, but I see a lot of use cases where an explicit api can help. Having a good documentation (be it as a test suite or as prose in a wiki) [helps newcomers](https://github.com/gesellix-docker/docker-client/issues/17#issue-94297435) to not be frustrated in the first five minutes of contact with a library.


