
+++
date = "2013-10-17"
draft = false
title = "Node.js Monitor"
slug = "node-js-monitor"
tags = ['nodejs', 'monitor', 'health check']
banner = ""
aliases = ['/node-js-monitor/']
+++

Playing around with node.js made me build a monitoring tool to perform continuous health checks.

I have an application running with a status servlet available under a URL like `http://example.com/healthcheck`. For a healthy system, I get a JSON as response including an attribute `result.summary`. In case that summary isn't OK, I want the monitor to send me an email with details.

Nothing spectacular, so you'll find the little piece (of currently untested) code at [GitHub](https://github.com/gesellix/node-monitor). Have fun!


