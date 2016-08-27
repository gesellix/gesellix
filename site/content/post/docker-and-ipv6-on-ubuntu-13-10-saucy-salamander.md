
+++
date = "2014-02-16"
draft = false
title = "Docker and IPv6 on Ubuntu 13.10 (Saucy Salamander)"
slug = "docker-and-ipv6-on-ubuntu-13-10-saucy-salamander"
tags = ['docker', 'ipv6', 'inet6', 'ubuntu', 'packet forwarding']
banner = ""
aliases = ['/docker-and-ipv6-on-ubuntu-13-10-saucy-salamander/']
+++

After making myself familiar with [Docker](https://www.docker.io/) I wanted to use it on a more recent [Ubuntu](http://www.ubuntu.com/) [13.10](http://releases.ubuntu.com/13.10/) release. I still didn't install Docker natively on my pc, but use a [Vagrant](http://www.vagrantup.com/) box to play with fresh releases. After downloading a fresh Ubuntu 13.10 image, creating a VirtualBox image and installing the current Docker release 0.8.0, I tried to use my other little toys [CouchDB](http://couchdb.apache.org/) and [Elasticsearch](http://www.elasticsearch.org/) in Docker containers. Sadly, I couldn't connect to the exposed ports anymore.

The Docker installation docs for Ubuntu Linux 13.04 and 13.10 mention the [configuration of UFW](http://docs.docker.io/en/latest/installation/ubuntulinux/#ufw) to modify the `DEFAULT_FORWARD_POLICY` to accept all traffic. Well, the UFW wasn't enabled. So the usual digging began, searching on StackOverflow, GitHub and developer blogs. Most hints mentioned disabling the IPv6 support via sysctl, but a quite clear statement of [Jérôme Petazzoni](https://twitter.com/jpetazzo) at a [StackOverflow answer](http://stackoverflow.com/questions/21093173/docker-container-without-ipv4-address#21102698) made me search for alternatives. 

Instead of disabling IPv6 some people found a way to enable IPv6 inside of containers: Andreas Neuhaus showed some native lxc commands to [make containers support IPv6](http://zargony.com/2013/10/13/ipv6-in-docker-containers). Marek Goldmann also shows some other use cases for native lxc commands to connect [containers on multiple hosts](http://goldmann.pl/blog/2014/01/21/connecting-docker-containers-on-multiple-hosts/). Well, hopefully a [pull request](https://github.com/dotcloud/docker/pull/2974) to make Docker natively support IPv6 will merged soon. My problem didn't look like missing IPv6 support inside the container, though.

Some debugging, bridge configuration, iptables fun and interface setups later I came back to the sysctl config and had a look at the existing entries. You might by surprised how well each default entry is documented and especially one entry looked promising: I enabled IPv6 forwarding on all interfaces by uncommenting the entry with: `net.ipv6.conf.all.forwarding=1` in the `/etc/sysctl.conf`. A quick reboot later finally showed a response from the dockerized CouchDB. Relax! Sometimes it's too easy.

Now comes the fun part with reconnecting the CouchDB River Plugin for ElasticSearch over different containers again :)


