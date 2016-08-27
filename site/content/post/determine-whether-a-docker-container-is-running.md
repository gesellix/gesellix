
+++
date = "2014-09-16"
draft = false
title = "Determine whether a Docker container is running"
slug = "determine-whether-a-docker-container-is-running"
tags = ['docker', 'running', 'container', 'json', 'jq', 'shell']
banner = ""
aliases = ['/determine-whether-a-docker-container-is-running/']
+++

You might want to find out if a Docker container named "elasticsearch" is currently running. There is a `docker ps` command to list all running containers in a table-like view. Lets assume there are two containers currently running, the result would look like this:
![](/images/2014/Sep/docker_ps_.png)

Ignoring the fact that it's a quite wide table you might want to take the chance and use some good old tools. Yes, the classics like `grep`, `awk`, `sed` and the other usual suspects. You only have to find a line with the last column to equal or contain "elasticsearch".

That's not very exciting. A hipster developer these days would prefer to use JSON, because... JSON. Luckily, when using Docker we can use the [Docker Remote API](https://docs.docker.com/reference/api/docker_remote_api/) to perform the same request the `docker ps` command did. Combined with a great tool like [jq](http://stedolan.github.io/jq/) you can try to get the same result. So, the first step would be to ask the Docker Remote API to list the running containers:
```
$ curl -X GET "http://172.17.42.1:2375/containers/json?all=false
[
  {
    "Command": "bash",
    "Created": 1410901503,
    "Id": "be2dd8aa82220a3b90a8712f47cfbbd482dbde7abd01f8c646bc3443a9ea04ab",
    "Image": "ubuntu:14.04",
    "Names": [
      "/silly_elion"
    ],
    "Ports": [],
    "Status": "Up 2 seconds"
  },
  {
    "Command": "/elasticsearch/bin/elasticsearch",
    "Created": 1410889877,
    "Id": "5250a96ebd16e72e664f31814f4a5a03df1ab7b50c52044f6a623002acca1ee0",
    "Image": "elasticsearch:latest",
    "Names": [
      "/elasticsearch"
    ],
    "Ports": [
      {
        "IP": "0.0.0.0",
        "PrivatePort": 9200,
        "PublicPort": 9200,
        "Type": "tcp"
      },
      {
        "IP": "0.0.0.0",
        "PrivatePort": 9300,
        "PublicPort": 9300,
        "Type": "tcp"
      }
    ],
    "Status": "Up 3 hours"
  }
]
```

We want to filter the `Names` array and test if one of both arrays from both containers equals our name "/elasticsearch". The leading slash is an internal detail to Docker, which is usually removed by the native Docker client.

So, we extract the `Names` property from both objects and check whether they equal our desired name. This is the intermediate result:
```
$ curl -X GET "http://172.17.42.1:2375/containers/json?all=false" \
    | ./jq '.[].Names | .[] | . == "/elasticsearch"'
false
true
```

We get two results, for each container, and each Names entry. But we wanted a single result, which tells us if one of all containers is the eleasticsearch container. So, let's combine the list to an array and reduce its entries to a single value:

```
$ curl -X GET "http://172.17.42.1:2375/containers/json?all=false" \ 
    | ./jq '[ .[].Names | .[] | . == "/elasticsearch" ] \
            | reduce .[] as $item (false; . | $item)'
true
```

Note the `[...]` around the filter of the previous step, which combines both results to a single array with two entries.

Well, the command doesn't look very simple, but I would say by explicitly using JSON properties it's far more stable than `grep`ing a pseudo-table. I also found the [jqplay](https://jqplay.org/) playground for checking the jq filter to be a big help. Just give it a try!


