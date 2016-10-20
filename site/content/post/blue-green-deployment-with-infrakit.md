
+++
date = "2016-10-20"
draft = false
title = "Blue/Green Deployment with Docker InfraKit"
slug = "blue-green-deployment-with-docker-infrakit"
tags = ['continuous deployment', 'blue/green deployment', 'docker', 'infrakit', 'automation']
banner = ""
aliases = ['/blue-green-deployment-with-infrakit/']
+++

The [Docker InfraKit](https://github.com/docker/infrakit) is a tool to create and manage you infrastructure in a declarative and self-healing manner.

InfraKit itself more or less only consists of plugins, communicating via unix domain sockets.

There are different types of plugins, namely _group_, _instance_, and _flavour_, each with a focus on different layers of infrastructure management.
Instance plugins are no surprise here: they manage your physical resources. Whether a physical resource is actually some machine or only a virtual concept, is an implementation detail of the instance plugin.
Managing distinct instances would be unhandy, so you can use group plugins as a tool to operate on a group of instances with similar characteristics.
The actual behaviour of your services on each instance of a group happens through flavour plugins. They define how to monitor services and which commands to run.

InfraKit is still under heavy development, which is your chance to give the maintainers some feedback or suggestions so that the tool and the growing ecosystem of plugins will work for your use cases.
It has been explicitly designed to manage your infrastructure, with the implication that it shouldn't be regarded as replacement to e.g. Docker swarm mode.

# Creating your local InfraKit

I started with the [tutorial](https://github.com/docker/infrakit/blob/master/docs/tutorial.md) you can find in the InfraKit repository.
Over time, there have already been huge improvements and breaking changes to the commands and configuration, so that you should always verify if your local config does still work.
Here is a list of commands to create the necessary binaries locally. I assume you have a working [Golang environment](https://github.com/docker/infrakit#building):

````
mkdir -p $GOPATH/src/github.com/docker
cd $GOPATH/src/github.com/docker
git clone git@github.com:/docker/infrakit.git
cd infrakit

make build-in-container
````

After running the commands above you should have all binaries in a new subdirectory `build`:

````
$ ls -l $GOPATH/src/github.com/docker/infrakit/build/
total 155720
-rwxr-xr-x  1 gesellix  staff  7780048 Oct 20 21:31 infrakit
-rwxr-xr-x  1 gesellix  staff  8757616 Oct 20 21:31 infrakit-flavor-combo
-rwxr-xr-x  1 gesellix  staff  9774560 Oct 20 21:31 infrakit-flavor-swarm
-rwxr-xr-x  1 gesellix  staff  8654128 Oct 20 21:31 infrakit-flavor-vanilla
-rwxr-xr-x  1 gesellix  staff  8666928 Oct 20 21:32 infrakit-flavor-zookeeper
-rwxr-xr-x  1 gesellix  staff  8889808 Oct 20 21:31 infrakit-group-default
-rwxr-xr-x  1 gesellix  staff  9183136 Oct 20 21:32 infrakit-instance-file
-rwxr-xr-x  1 gesellix  staff  9308320 Oct 20 21:32 infrakit-instance-terraform
-rwxr-xr-x  1 gesellix  staff  8697344 Oct 20 21:32 infrakit-instance-vagrant
````

# Using InfraKit to perform deployments 

I wanted to see how InfraKit feels when trying to use it as [blue/green deployment](http://martinfowler.com/bliki/BlueGreenDeployment.html) utility.
As mentioned above, that's not exactly what InfraKit has been built for, but let's see what happens.

Let's bootstrap a basic InfraKit environment by running some plugins. Exactly like described in the tutorial, I use the file instance plugin to create virtual instances represented as files.
The default group plugin and vanilla flavour plugin are also used to make a local setup as easy as possible. So, let's start the plugins as background tasks:

````
build/infrakit-group-default &
mkdir -p tutorial
build/infrakit-instance-file --dir ./tutorial/ &
build/infrakit-flavor-vanilla &
````

The command `build/infrakit plugin ls` should respond with a list of the three mentioned plugins:

````
Plugins:
NAME                LISTEN
flavor-vanilla      /Users/gesellix/.infrakit/plugins/flavor-vanilla
group               /Users/gesellix/.infrakit/plugins/group
instance-file       /Users/gesellix/.infrakit/plugins/instance-file
````

You can find the unix socket file handles in the column `LISTEN` for each plugin. You can use the unix sockets to send commands to the plugins using a HTTP api.
The InfraKit cli at `build/infrakit` makes that task a bit more convenient. 

You can list the current instances by querying the instance plugin:
 
````
build/infrakit instance --name instance-file describe
````

We didn't tell the instance plugin about any instances, yet, so the list should be empty.
The group plugin accepts a new configuration in JSON format, either via `STDIN` or files. I created a subdirectory for those config files:

````
mkdir -p tutorial-config
````

Now let's define a new group, called "app-blue":

````
cat << EOF > tutorial-config/app-blue-group.json
{
  "ID": "app-blue",
  "Properties": {
    "Allocation": {
      "Size": 2
    },
    "Instance": {
      "Plugin": "instance-file",
      "Properties": {
        "Note": "Instance properties app version 1.0"
      }
    },
    "Flavor": {
      "Plugin": "flavor-vanilla",
      "Properties": {
        "UserData": [
          "docker run -dit -p 80:80 nginx:alpine"
        ],
        "Labels": {
          "tier": "web",
          "project": "app",
          "colour": "blue"
        }
      }
    }
  }
}
EOF
````

You can recognize dedicated configuration blocks for the instance, and flavour plugins. The file instance plugin doesn't do very much, but it will be labelled with the `Note`.
The flavour plugin makes things actually happen by running an Nginx container listening on port 80 and configuring some labels.
Since we're describing a group here, it will need an `ID`, in this case I chose `app-blue`.

The configuration can now be passed to the group plugin, so that it registers a new group `app-blue` and passes the other configuration blocks to the chosen plugins:
 
````
build/infrakit group watch tutorial-config/app-blue-group.json
````

The group plugin also watches the new group for changes and automatically acts in a way to converge the actual state to the desired state.
You can easily verify that behaviour by deleting one of the instances (by deleting a file in the subdirectory `tutorial`) and watching it re-creating another instance:

````
$ ls tutorial/
instance-6050337735652914571    instance-8310575841542371925
$ rm tutorial/instance-6050337735652914571
INFO[5731] Adding 1 instances to group to reach desired 2 
INFO[5731] Created instance instance-7932269456152577966 with tags map[infrakit.config_sha:l9lqpBGJSWIrDOtrliJRGSK1y60= infrakit.group:app-blue] 
$ ls tutorial/
instance-7932269456152577966    instance-8310575841542371925
````

The `inspect` sub-command gives you an overview on your group:

````
$ build/infrakit group inspect app-blue
ID                            LOGICAL          TAGS
instance-7932269456152577966    -              infrakit.config_sha=l9lqpBGJSWIrDOtrliJRGSK1y60=,infrakit.group=app-blue
instance-8310575841542371925    -              infrakit.config_sha=l9lqpBGJSWIrDOtrliJRGSK1y60=,infrakit.group=app-blue
````

Let's add the `app-green` group:

````
cat << EOF > tutorial-config/app-green-group.json
{
  "ID": "app-green",
  "Properties": {
    "Allocation": {
      "Size": 2
    },
    "Instance": {
      "Plugin": "instance-file",
      "Properties": {
        "Note": "Instance properties app version 2.0"
      }
    },
    "Flavor": {
      "Plugin": "flavor-vanilla",
      "Properties": {
        "UserData": [
          "docker run -dit -p 81:80 nginx:alpine"
        ],
        "Labels": {
          "tier": "web",
          "project": "app",
          "colour": "green"
        }
      }
    }
  }
}
EOF

build/infrakit group watch tutorial-config/app-green-group.json
````

Nothing special here, I only changed some details and the port binding.

Please note that the current demo setup creates instances as files, but doesn't actually run the Nginx containers.

Now let's assume that we want to deploy a new variant of our Nginx container, because we forgot to add a necessary environment parameter.
You can either choose to modify the previously created `tutorial-config/app-blue-group.json` configuration or create a new one like this: 

````
cat << EOF > tutorial-config/app-blue-group-2.json
{
  "ID": "app-blue",
  "Properties": {
    "Allocation": {
      "Size": 2
    },
    "Instance": {
      "Plugin": "instance-file",
      "Properties": {
        "Note": "Instance properties app version 3.0"
      }
    },
    "Flavor": {
      "Plugin": "flavor-vanilla",
      "Properties": {
        "UserData": [
          "docker run -dit -p 80:80 -e VERSION=2 nginx:alpine"
        ],
        "Labels": {
          "tier": "web",
          "project": "app",
          "colour": "blue"
        }
      }
    }
  }
}
EOF
````

InfraKit won't automatically apply those changes now, and you can ask it which actions it would execute when the new config would be applied:

````
$ build/infrakit group describe tutorial-config/app-blue-group-2.json 
app-blue : Performs a rolling update on 2 instances
````

# InfraKit and blue/green deployment

How can InfraKit be used in a blue/green deployment? Since InfraKit knows your instances, groups, and flavours, it becomes easy
for you to describe the desired state of your whole application setup. Similarly, applying changes becomes easy, too!

[Blue/green deployment](http://martinfowler.com/bliki/BlueGreenDeployment.html) is a concept to allow continuous deployment without interrupting your clients' interactions with your app.
Your clients' don't care about your deployment, in fact: they don't want to be disturbed by technical details. So, in essence, blue/green deployment
describes how to manage different versions of your app and switching between them with the help pf a reverse proxy in front of them.
Deployments are a multi-step process, where a new version is deployed as an "offline" version and afterwards the reverse proxy is reconfigured to use that fresh release instead of the old one.

Question is: how do you perform your deployments? Some use shell scripts, some use tools originally designed for provisioning (e.g. Puppet or Ansible, which [I described in another article](https://github.com/gesellix/pipeline-with-gradle-and-docker/blob/master/articles/part5.md#ansible-for-application-deployment)), some might leverage modern orchestration tools.
Well, the new kid is InfraKit and it could be used to perform your rolling deployments.

As you've seen above, performing a single deployment isn't very hard, the only missing bit is the reverse proxy and some little mechanism to re-configure
that proxy. But that's the same solution for any other tool out there, maybe it's integrated into your tool or you simply add a single shell command somewhere.

The significant value of InfraKit to me is: it behaves in a resilient way and it feels like a combination of cluster management and cron. Not in a way cron
runs tasks which end after having finished their actions. If you know about regular puppet agent runs to regularly verify the desired state of your machines, you probably know what I mean.
InfraKit takes your desired configuration once and then is your Watchmen for your whole group.

You have seen how InfraKit performs actions when your infrastructure doesn't look like your desired infrastructure.
You have also seen how it tells you about the actions it's going to perform when changes would be applied. You can apply the changes now:

````
$ build/infrakit group update tutorial-config/app-blue-group-2.json 
INFO[9857] Executing update plan for 'app-blue': Performs a rolling update on 2 instances 
INFO[9867] Scaler has quiesced                          
INFO[9867] Found 2 undesired instances                  
INFO[9867] Destroying instance instance-7932269456152577966 
INFO[9871] Adding 1 instances to group to reach desired 2 
INFO[9871] Created instance instance-5485092084438864736 with tags map[infrakit.config_sha:jHUgS68HiWOOPrTmbHy00-YV9QI= infrakit.group:app-blue] 
INFO[9877] Scaler has quiesced                          
INFO[9877] Found 1 undesired instances                  
INFO[9877] Destroying instance instance-8310575841542371925 
INFO[9881] Adding 1 instances to group to reach desired 2 
INFO[9881] Created instance instance-8719089717303567911 with tags map[infrakit.config_sha:jHUgS68HiWOOPrTmbHy00-YV9QI= infrakit.group:app-blue] 
INFO[9887] Scaler has quiesced                          
INFO[9887] Finished updating group app-blue             
update app-blue completed
````

InfraKit destroys and creates complete instances for you, which is probably a bit unusual when you think about your current deployment.
You're probably used to only stopping and creating containers, but not whole instances. The thing is: it depends on the instance plugin you choose.
I'm not aware of a docker instance plugin or something more granular, but InfraKit would allow you to create one very quickly and specific for your needs.

# Outlook

What I wanted to show is another perspective on the tutorial, and show an option how to perform deployments.
Since InfraKit is still in an early state there are some options missing - consider security management or notifications to the admin when InfraKit 
needs to react on an invalid state. Nevertheless there is a huge potential to improve the current state of infrastructure
management and maybe even service deployment.

The idea behind InfraKit (and SwarmKit being available in the Docker engine) with consensus driven protocols and flexible plugins
has a huge potential to make our lifes easier in the near future. Now is the time to start playing with the new concepts!

You should watch the Docker repos for new plugins, e.g. like the [AWS plugin](https://github.com/docker/infrakit.aws),
or discuss with other adopters in the Docker Community [#Infrakit Channel](https://dockercommunity.slack.com/archives/infrakit).

# P.S.

Destroying your infrastructure is maybe too easy:

````
build/infrakit group destroy app-blue
build/infrakit group destroy app-green
````
