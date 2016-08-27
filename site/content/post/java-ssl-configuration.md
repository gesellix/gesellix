
+++
date = "2012-02-15"
draft = false
title = "Java SSL Configuration"
slug = "java-ssl-configuration"
tags = ['java', 'ssl', 'gesellix.de', 'tomcat', 'keystore', 'config']
banner = ""
aliases = ['/java-ssl-configuration/']
+++

Working with external interfaces often needs a secured connection, mostly implemented using SSL. I recently ran into some fresh setup of two hosts, sending each other SOAP requests via HTTPS.

Being a Java developer at my office, I got some error messages quite unknown to me, but after some reading of blogs and with other informational sources the problems had been fixed. Understanding the concept behind SSL and how the SSL handshake works are crucial when trying to understand error messages and to know where to fix them.

In case you are trying to use SSL connections with certificates in combination with Java you may have a look at a little how-to I wrote at my employers [Hypoport IT Blog](http://blog-it.hypoport.de/2012/02/15/java-ssl-konfiguration-mit-keystores/). It's written in German, but I guess you can understand most parts. Most of its content is taken from [another article](http://billcomer.blogspot.com/2010/03/ssl-tomcat-and-self-signed-certificates.html), enhanced with additional tips and solutions for special issues.

