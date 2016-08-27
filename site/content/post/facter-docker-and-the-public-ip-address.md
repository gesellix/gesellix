
+++
date = "2014-03-02"
draft = false
title = "Facter, Docker and the public ip address"
slug = "facter-docker-and-the-public-ip-address"
tags = ['docker', 'puppet', 'facter', 'ip address', 'ipaddress', 'custom fact', 'override']
banner = ""
aliases = ['/facter-docker-and-the-public-ip-address/']
+++

Using [Docker](https://www.docker.io/) on a [Puppet](http://puppetlabs.com/) managed host influences [Facter](http://puppetlabs.com/facter) when it tries to find the host ip address.

#####Which network interface is the best?
Facter collects some so called facts about the system and provides them to Puppet modules. When using a fact like `:ipaddress` you'll see that Facter only uses the output of the native `ifconfig` command, sorts all existing interfaces by name and takes the first non local interface as result. Facter then sets `:ipaddress`, `:macaddress` and `:netmask` as provided by that interface.

Most Linux based systems use `eth0` as interface name for the public interface. This seems to be ok in most cases, but after installing Docker you'll see an additional interface `docker0`. Facter now reads the network configuration from the Docker interface, which can lead to problems in your Puppet modules.

The same problem also arises without Docker when you have more than one interface installed. Which interface would you Facter expect to use, `eth0` or `eth1`?

#####Telling Facter the truth

Confronting your favourite search tool with the described behaviour (you're never the first person having your problem, don't ya?) should link you to the PuppetLabs Q&A page about the [issue](https://ask.puppetlabs.com/question/5112/how-to-force-facter-not-to-use-private-ip-address/). The given answer provides three options to overcome the problem:
1. File a bugreport
2. Write a [custom fact](http://docs.puppetlabs.com/guides/custom_facts.html) `ipaddress_primary` that returns your desired value
3. Use `ipaddress_eth0` instead of `ipaddress`

Filing a bugreport is probably not a good idea, since Facter cannot know enough about which interface you expect. Using the dedicated `ipaddress_eth0` should be valid, when you can be sure that the interface name is static, e.g. by setting it in your Puppet modules. Sadly, I couldn't use the third option, because I had different interface names on different servers.

Just for the record: there's at least a fourth option: manually set Docker's interface name so that it appears after `eth0` in the sorted list of interfaces. Well, sometimes you can't simply change interface names, and I preferred to make Facter work as expected without changing the world around it.

#####Overriding facts
So I tried to write a custom fact - the documentation helped a lot and it's quite easy. I had the idea of overriding the built in `:ipaddress` fact, but that doesn't seem to be possible by using custom facts. Luckily, PuppetLabs have provided a way of [overriding facts](http://www.puppetcookbook.com/posts/override-a-facter-fact.html) by the use of environment variables: instead of adding custom facts, you can set a variable like `FACTER_ipaddress="192.168.178.42"`.

Facter accepts any fact name after the prefix `FACTER_`, so you can override any fact you like. In my case the ip addresses are static, so this is a very convenient way of making Factor work together with Docker. When using dynamic ip addresses, you should check if any of the other suggestions above work for you.

You can manage `/etc/environment` with Puppet, so the environment variables are available without manually editing files on a server. My `/etc/environment` now looks like this:
```
FACTER_ipaddress="192.168.178.42"
FACTER_netmask="255.255.255.0"
```
Happy shipping!


