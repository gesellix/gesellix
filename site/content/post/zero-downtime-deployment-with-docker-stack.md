
+++
date = "2017-05-22"
draft = true
title = "Zero Downtime Deployment with Docker Stack and Spring Boot"
slug = "zero-downtime-deployment-with-docker-stack-and-spring-boot"
tags = ['continuous deployment', 'zero downtime deployment', 'docker', 'docker-stack', 'docker-services', 'spring-boot']
banner = ""
aliases = ['/zero-downtime-deployment-with-docker-stack-and-spring-boot/']
+++

Playing around with Docker Swarm really makes fun: you only need a single command
to initialize a cluster on your local machine. The following line configures your Docker Engine
as Docker Swarm manager:

    docker swarm init

The command output already tells you how to add additional worker nodes and looks similar to this:

    docker swarm join \
    --token SWMTKN-1-somecharacters-andmorecharacters \
    192.168.47.11:2377

You don't necessarily have to add additional worker nodes, because the manager node can also be used as worker.
If you wonder how to add more manager nodes, the Engine will help you if you enter this one:

    docker swarm join-token manager

In your production environment you might be tempted to have a more resilient setup, using
3 or 5 Swarm manager nodes (to build a quorum) and even more worker nodes depending on your workload.

Docker Swarm will then manage your services with their tasks to be deployed on your cluster. Automated
restarts, rolling updates, networking, internal DNS, simple load balancing, and built-in security
are some of the features you get for free and without much hazzle.

But why all the fuzz about that? Let's first take a look at our status quo in my team.
If you want to skip the gossip and continue with the real stuff, just head over to the [relevant section below](#the-awakening).

# The Good

We already posted an article series about the way we implemented [a continuous deployment pipeline](http://tech.europace.de/a-continuous-deployment-pipeline-with-gradle-and-docker/).
The underlying concept hasn't changed too much, so even the [code samples on GitHub](https://github.com/gesellix/pipeline-with-gradle-and-docker)
are still a good reference if you want to start with a small application with a small number of services.

Meanwhile, our code base has grown - which is certainly a good thing. We still rely on Ansible to perform
provisioning and blue-green deployments. The number of services has grown, though. More advanced stuff has been added,
e.g. Consul (-template) in combination with Registrator, and NGINX as reverse proxy. Our setup isn't very
special, there are plenty of articles out there for such a setup and you can find very
[concise](https://github.com/shcoderAlex/docker-consul-registrator-nginx-proxy) [examples](https://github.com/ziyasal-archive/confroxy)
to [get you started](https://github.com/avthart/docker-consul-template/blob/master/examples/examples.md).

Our current setup makes it quite easy to add yet another microservice into our infrastructure. Since we
wrote every Ansible role and playbook ourselves, we know where to tweak our settings or where to fix
issues. Yet, such a setup with Consul/Registrator/NGINX isn't trivial to maintain and using Ansible
for deployments still feels a bit strange.

# The Bad?

I personally have the impression that Ansible is very good at provisioning your nodes. But when it
comes down to performing `docker run`, you'll feel that the Docker module in an Ansible role doesn't really
comply with Ansible's claim to be declarative. It works, it has become stable and can handle different
Docker Engine versions, but it doesn't feel right.

When I look at an actual deployment, where our TeamCity goal runs an Ansible image to internally use `docker-py`,
talking to a Docker Engine on another node and ultimately triggers the `docker pull` and `docker run` api commands,
I wish for less abstractions.

Consider the alternative: TeamCity performs a simple `docker -H target.node.local:2376 service update ...`.

Nothing more. Yeah, that's kind of an understatement, but you get the idea.

Ansible helped us to drop shell scripts when we started to scale our deployment pipeline with the growing number
of services and nodes. In fact, we can consider TeamCity + Ansible + Consul + Registrator + Consul Template to be
"our orchestration tool". Over time, alternatives have shown up, and if I look at the shiny features
of tools like Swarm, Kubernetes, and DC/OS, I ask myself why I should maintain Ansible roles along with
the non-trivial setup of our home grown orchestration tool.

Maybe you already know that article about the [Configuration Complexity Clock](http://mikehadlow.blogspot.de/2012/05/configuration-complexity-clock.html).
If not, please go and read it! I'll wait for you to come back here.

...

I wouldn't really say that we should go full circle around that clock. I would prefer to find better tools
and stay at, don't know, maybe 4 o'clock? Maybe what we need is a little bit of every hour on that clock?

Yes. I want the hard coded actual bit to perform a container deployment. But I don't want to maintain it myself.
So I'll need to configure that externally maintained code to fit my needs. I wouldn't really need a full fledged
rules engine or a special DSL, if the tool of choice is simple enough to use.

There comes the tricky part: _fit my needs - simple to use_. You might argue that a generic tool won't be possible
with such constraints. And I guess you're right.

# The Ugly

We have some special use cases on some services. Yep, exceptions to a generic pattern are evil, but without exceptions
we would be quite bored, hm? Let's dig into the interesting bit: in most cases, our platform needs to perform requests
to several of our linked partners, external rating services, and document stores. As you might guess, there are
some services which are not as fast as we'd prefer them to be. We actually have timeouts in the range of several minutes.

That's why we need to consider long running requests during our continuous deployments. Using blue-green deployment,
we have the option to deploy new releases of our service, use those for new incoming requests, but keep our old
instances running for several minutes. That way, pending connections won't be cut during a certain timeout.

Can you implement such a scenario with any orchestration tool? Well, I'm not aware of a simple tool to fit such needs.
I consider Docker Swarm to be very simple to use, but it sadly won't keep pending connections after service updates.

Really? Well, not quite.

# A New Hope

Luckily we're not the only ones to strive for zero downtime deployment. Some people out there use Spring Boot,
our application environment, and some people use Docker. Some use both, just like us. Some want their servlet
container to shut down gracefully (see [spring-projects/spring-boot/4657](https://github.com/spring-projects/spring-boot/issues/4657)),
and some want to perform rolling upgrades with Docker (see [moby/moby/30321](https://github.com/moby/moby/issues/30321)).

We cannot expect from either Spring Boot or Docker, now also known as Moby, to generically keep pending connections
and block a container shutdown. 

But Brian Goff's [suggestion](https://github.com/moby/moby/issues/30321#issuecomment-296261856) to handle the `TERM` signal
inside our application made us dig a bit deeper into JVM shutdown hooks.
Reading the Runtime Javadoc about [addShutdownHook()](https://docs.oracle.com/javase/8/docs/api/java/lang/Runtime.html#addShutdownHook-java.lang.Thread-)
made us wonder whether the JVM would accept our idea to block the shutdown for several minutes. In fact, you cannot simply ignore
a statement like _Shutdown hooks should also finish their work quickly_. You never know if you don't try, so we gave
it a try and using Andy Wilkinson's [code snippet](https://github.com/spring-projects/spring-boot/issues/4657#issuecomment-161354811)
made it easy for us to create an example application.

# The Awakening 

An example application is available at [gesellix/graceful-shutdown-spring-boot](https://github.com/gesellix/graceful-shutdown-spring-boot).
Since we wanted to check a possible Docker Services setup as potential replacement for our Ansible based deployments,
the example app can easily be [deployed as a Docker Stack](https://github.com/gesellix/graceful-shutdown-spring-boot#docker-stackservice).
If you're not familiar with Docker Stacks, I recommend you to read the little introduction at [docs.docker.com](https://docs.docker.com/engine/swarm/stack-deploy/).

You can consider a Docker Stack to be the extended version of Docker Compose. The difference lies in the additional options
to configure replicas, rolling update policies, and service constraints. The most important difference to Compose is probably
the service deployment across several nodes. Everything is powered by Docker Swarm, so most you know about Swarm and Docker Services
also applies to Stacks.

Back to our example stack: it consists of [Træfik](https://traefik.io/) as Docker aware reverse proxy and the example app as replicated Spring Boot service.
To ease testing the shutdown hook timeout, a delay can be configured via Spring Boot mechanisms using the `catalina.threadpool.execution.timeout.seconds`
property. Its value defaults to `30` seconds. Docker also needs to be aware of our delay, so that it won't `SIGKILL` the service
instances after 10 seconds. The necessary properties (`stop-grace-period` and `update-config.delay`) are already configured
in the [stack file](https://github.com/gesellix/graceful-shutdown-spring-boot/blob/825b56761c217dcf607f39f4c799b4414eb3a4fe/stack.yml) with a value of 60 seconds. 

# Get Real

Starting the full stack works like described below. If you didn't already initialize your swarm you're going to need it now:

    docker swarm init 

Then, clone or download the [gesellix/graceful-shutdown-spring-boot](https://github.com/gesellix/graceful-shutdown-spring-boot) repository
and change into the _graceful-shutdown-spring-boot_ directory. You should find a `stack.yml` file in the repository root.

With the following command you'll advice Docker to create a virtual network named _traefik_, download the necessary Docker images and create
the configured services _traefik_ and _app_. The stack will be named `grace`:

    docker stack deploy --compose-file stack.yml grace

When all services are running (you can check their current state via `docker stack ps grace`),
please open your browser at [http://localhost](http://localhost). You should see a little web page with two columns, each
with a button. The left one allows you to check the basic connectivity by calling the app's echo endpoint. The button in the
right column allows you to simulate a long running request by generating an endless stream of random bytes. If you click that
button, the blue area at the bottom should show an increasing number of received bytes.

You can follow the service logs with:

    docker service logs -f grace_app

A service update with task downtime can be triggered e.g. by adding a new environment variable. Please use a new terminal window
if you're already following the service logs. 

    docker service update --env-add "foo=bar" grace_app

The logs should emit log messages like this one:

> grace_app.1.ki669xys5x6x@moby    | 2017-05-23 12:34:31.981  WARN 1 --- [       Thread-3] d.g.d.zerodowntime.GracefulShutdown      : Context closed. Going to await termination for 30 SECONDS.

Docker will randomly choose either `grace_app.1` or `grace_app.2`, and your endless request should keep one of both delaying the
shutdown for 30 seconds. After that delay, a new log message should appear:

> grace_app.1.ki669xys5x6x@moby    | 2017-05-23 12:34:01.989  WARN 1 --- [       Thread-3] d.g.d.zerodowntime.GracefulShutdown      : Tomcat thread pool did not shut down gracefully within 30 SECONDS. Proceeding with forceful shutdown

So, the application paused the shutdown for 30 seconds, and Docker didn't forcefully kill the container. If you have a look at
your browser window, the increasing number of received bytes have stopped.
