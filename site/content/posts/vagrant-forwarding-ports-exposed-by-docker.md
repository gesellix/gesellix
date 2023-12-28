
+++
date = "2013-11-05"
draft = false
title = "Vagrant Forwarding Ports Exposed by Docker"
slug = "vagrant-forwarding-ports-exposed-by-docker"
tags = ['elasticsearch', 'couchdb', 'docker', 'vagrant', 'port forwarding']
banner = ""
aliases = ['/vagrant-forwarding-ports-exposed-by-docker/']
+++

Playing around with [docker](http://www.docker.io/) running inside a [Vagrant](http://www.vagrantup.com/) VM and trying to use some services being exposed via HTTP ports makes you ask how to automatically [forward](http://docs.vagrantup.com/v2/networking/forwarded_ports.html) the exposed docker ports through Vagrant to the host system. _phew_

I found an already merged [pull request](https://github.com/dotcloud/docker/pull/857), which looked like what I wanted. So, after a peek into the docker Vagrant file I tried to expose a [CouchDB](http://couchdb.apache.org/) port to the host system like this:
```
$host> FORWARD_DOCKER_PORTS='true' vagrant up
$host> vagrant ssh
$vagrant> docker run -d -p 49815:5984 -i -t gesellix/docker-example
$host> curl -X GET "http://localhost:49815"
```
It just worked! If you'd like to have a look at my example project, you can find it at [GitHub](https://github.com/gesellix/docker-playground). I'm going to continue building a complete application backend including CouchDB, [ElasticSearch](http://www.elasticsearch.org/) and other toys. You might have better docker or Vagrant knowledge than me, so if you'd have any hints, I'd really like some [feedback](https://github.com/gesellix/docker-playground/issues). Thanks!


