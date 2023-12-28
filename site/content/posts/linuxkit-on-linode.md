
+++
date = "2017-06-18"
draft = false
title = "Running Docker LinuxKit on Linode"
slug = "running-docker-linuxkit-on-linode"
tags = ['docker', 'linuxkit', 'linode', 'kvm']
banner = ""
aliases = ['/running-docker-linuxkit-on-linode/']
+++

This post will show you the steps it takes to run a custom [LinuxKit](https://github.com/linuxkit/linuxkit) based image on [Linode](https://www.linode.com/).

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">This looks so simple as it is: Running <a href="https://twitter.com/hashtag/Docker?src=hash">#Docker</a> <a href="https://twitter.com/hashtag/linuxkit?src=hash">#linuxkit</a> on a <a href="https://twitter.com/linode">@linode</a> <a href="https://t.co/rhVoFaCWE1">pic.twitter.com/rhVoFaCWE1</a></p>&mdash; Tobias Gesellchen (@gesellix) <a href="https://twitter.com/gesellix/status/876189014516281345">June 17, 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

# About LinuxKit

But let's start with the basics: LinuxKit is a tool to create immutable and minimal operating system images.
As you might expect, it heavily leverages Docker images and uses containers to run services via `containerd`.

Due to its simplicity you can configure your OS images with simple YAML files.
[Many examples](https://github.com/linuxkit/linuxkit/tree/master/examples) are already available in the LinuxKit GitHub repository.
I picked the [sshd.yml](https://github.com/linuxkit/linuxkit/blob/98028d417b6efae00992b8a122173d12ba1730d8/examples/sshd.yml) as a start.

There are several main sections to configure the desired target image, e.g. the underlying Kernel, init processes, boot time executables, and
the relevant services you'd like to run. Some sections like `files` allow to add custom files or specific configuration at build time.

A LinuxKit config to run a sshd server looks like this, as taken from the LinuxKit repo:

    # examples/sshd.yml
    kernel:
      image: "linuxkit/kernel:4.9.x"
      cmdline: "console=ttyS0 page_poison=1"
    init:
      - linuxkit/init:17693d233dd009b2a3a8d23673cb85969e1dce80
      - linuxkit/runc:3a4e6cbf15470f62501b019b55e1caac5ee7689f
      - linuxkit/containerd:04880f344709830aa4c938baa765764e644fc973
      - linuxkit/ca-certificates:75cf419fb58770884c3464eb687ec8dfc704169d
    onboot:
      - name: sysctl
        image: "linuxkit/sysctl:3aa6bc663c2849ef239be7d941d3eaf3e6fcc018"
    services:
      - name: getty
        image: "linuxkit/getty:d0765e0a14733f9454010ac109a7c846a4e67fc5"
        env:
         - INSECURE=true
      - name: rngd
        image: "linuxkit/rngd:1fa4de44c961bb5075647181891a3e7e7ba51c31"
      - name: dhcpcd
        image: "linuxkit/dhcpcd:7d2b8aaaf20c24ad7d11a5ea2ea5b4a80dc966f1"
      - name: sshd
        image: "linuxkit/sshd:abc1f5e096982ebc3fb61c506aed3ac9c2ae4d55"
    files:
      - path: root/.ssh/authorized_keys
        source: ~/.ssh/id_rsa.pub
        mode: "0600"
        optional: true
    trust:
      org:
        - linuxkit

I guess if you already know Docker, there's nothing special to it. The interesting aspect is the usage of content hashes
as tags, which you might be a bit unused with.

As the LinuxKit Readme already tells you how to get started, I'll only post the bare commands I used for your convenience:

    go get -u github.com/moby/tool/cmd/moby
    go get -u github.com/linuxkit/linuxkit/src/cmd/linuxkit
    git clone https://github.com/linuxkit/linuxkit
    cd linuxkit
    moby build -output iso-bios examples/sshd.yml

I assume you have [Golang](https://golang.org/) already installed and [Docker](https://www.docker.com/get-docker) is running.

The exciting part is probably the last command where the `moby` tool is used to create a standard ISO image based on the `sshd.yml` config.
When you start the command for the first time you'll see `moby` downloading and processing the referenced Docker images,
adding your SSH public key, and creating the desired output image as ISO format:

    $ moby build -output iso-bios examples/sshd.yml 
    Extract kernel image: linuxkit/kernel:4.9.x
    Pull image: docker.io/linuxkit/kernel:4.9.x@sha256:1631c1ceea2007b308ae4efeee9179c1e7d578a5dedab54fbcc64746532f2828
    Add init containers:
    Process init image: linuxkit/init:17693d233dd009b2a3a8d23673cb85969e1dce80
    Pull image: docker.io/linuxkit/init:17693d233dd009b2a3a8d23673cb85969e1dce80@sha256:cb2c1a01777004f34e4e1400a1deab0c7c68e252f97d5387a6708e59483228ef
    Process init image: linuxkit/runc:3a4e6cbf15470f62501b019b55e1caac5ee7689f
    Pull image: docker.io/linuxkit/runc:3a4e6cbf15470f62501b019b55e1caac5ee7689f@sha256:e8603bafe28d72887a2db01886d326a6e309e6ad3b2ad88bb7cee9be260d2fc7
    Process init image: linuxkit/containerd:04880f344709830aa4c938baa765764e644fc973
    Pull image: docker.io/linuxkit/containerd:04880f344709830aa4c938baa765764e644fc973@sha256:dcf0518979f3611003d0459458f9a260d9f95cfe73afce034a3aef447a8e2b71
    Process init image: linuxkit/ca-certificates:75cf419fb58770884c3464eb687ec8dfc704169d
    Pull image: docker.io/linuxkit/ca-certificates:75cf419fb58770884c3464eb687ec8dfc704169d@sha256:4bd4053003322a35f1effce6aa42066b22b5d9ea7dc638ef2f804df3b3b644f2
    Add onboot containers:
      Create OCI config for linuxkit/sysctl:3aa6bc663c2849ef239be7d941d3eaf3e6fcc018
    Pull image: docker.io/linuxkit/sysctl:3aa6bc663c2849ef239be7d941d3eaf3e6fcc018@sha256:189df608e87f237463858c86788da44b29e0bd8bd1a97fff7fcf7d32c1250edb
    Add service containers:
      Create OCI config for linuxkit/getty:d0765e0a14733f9454010ac109a7c846a4e67fc5
    Pull image: docker.io/linuxkit/getty:d0765e0a14733f9454010ac109a7c846a4e67fc5@sha256:20bf26fa27071e02c83bc6d7ffa508687986051db04199b5ef9233e0395afe07
      Create OCI config for linuxkit/rngd:1fa4de44c961bb5075647181891a3e7e7ba51c31
    Pull image: docker.io/linuxkit/rngd:1fa4de44c961bb5075647181891a3e7e7ba51c31@sha256:711f86b810c78f9be4d8b343053c14cfc5aa5a4ae939b398e3f3d95bbb900ce9
      Create OCI config for linuxkit/dhcpcd:7d2b8aaaf20c24ad7d11a5ea2ea5b4a80dc966f1
    Pull image: docker.io/linuxkit/dhcpcd:7d2b8aaaf20c24ad7d11a5ea2ea5b4a80dc966f1@sha256:b1bef35accd165a4235ad301f9bef6544922cb6eafdb60268b05d8c9d0b1566b
      Create OCI config for linuxkit/sshd:abc1f5e096982ebc3fb61c506aed3ac9c2ae4d55
    Pull image: docker.io/linuxkit/sshd:abc1f5e096982ebc3fb61c506aed3ac9c2ae4d55@sha256:727da1ef4a3f61050ed8164244610388f85578aea295b54a02d7b87c72b814a9
    Add files:
      root/.ssh/authorized_keys
    Create outputs:
      sshd.iso

You could also choose to create other output formats like the default `kernel+initrd` or a `raw` format for AWS.
When using the default output format you can even test your created image on your local machine by simply booting it.
This is how it looks like when running on Docker for Mac:

    $ moby build -output kernel+initrd examples/sshd.yml
    ...
    Create outputs:
      sshd-kernel sshd-initrd.img sshd-cmdline
    $ linuxkit run sshd
    virtio-net-vpnkit: initialising, opts="path=/Users/gesellix/Library/Containers/com.docker.docker/Data/s50"
    virtio-net-vpnkit: magic=VMN3T version=1 commit=0123456789012345678901234567890123456789
    Connection established with MAC=02:50:00:00:00:03 and MTU 1500
    vsock init 2:0 = sshd-state, guest_cid = 00000003
    early console in extract_kernel
    input_data: 0x0000000001ee53b4
    input_len: 0x000000000070f533
    output: 0x0000000001000000
    output_len: 0x00000000015e23e4
    kernel_total_size: 0x00000000011c6000
    booted via startup_32()
    Physical KASLR using RDRAND RDTSC...
    Virtual KASLR using RDRAND RDTSC...
    
    Decompressing Linux... Parsing ELF... Performing relocations... done.
    Booting the kernel.
    [    0.000000] Linux version 4.9.32-linuxkit (root@9ac68176ac52) (gcc version 6.3.0 (Alpine 6.3.0) ) #1 SMP Thu Jun 15 20:49:23 UTC 2017
    ...
    [    1.874566] Freeing unused kernel memory: 976K (ffffa135b2d0c000 - ffffa135b2e00000)
    
    Starting containerd
    
    Welcome to LinuxKit
    
                            ##         .
                      ## ## ##        ==
                   ## ## ## ## ##    ===
               /"""""""""""""""""\___/ ===
          ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
               \______ o           __/
                 \    \         __/
                  \____\_______/
    
    INFO[0000] starting containerd boot...                   module=containerd
    INFO[0000] starting debug API...                         debug="/run/containerd/debug.sock" module=containerd
    INFO[0000] loading plugin "io.containerd.content.v1.content"...  module=containerd type=io.containerd.content.v1
    INFO[0000] loading plugin "io.containerd.snapshotter.v1.btrfs"...  module=containerd type=io.containerd.snapshotter.v1
    INFO[0000] loading plugin "io.containerd.snapshotter.v1.overlayfs"...  module=containerd type=io.containerd.snapshotter.v1
    INFO[0000] loading plugin "io.containerd.differ.v1.base-diff"...  module=containerd type=io.containerd.differ.v1
    INFO[0000] loading plugin "io.containerd.metadata.v1.bolt"...  module=containerd type=io.containerd.metadata.v1
    INFO[0000] loading plugin "io.containerd.grpc.v1.containers"...  module=containerd type=io.containerd.grpc.v1
    INFO[0000] loading plugin "io.containerd.grpc.v1.content"...  module=containerd type=io.containerd.grpc.v1
    INFO[0000] loading plugin "io.containerd.grpc.v1.diff"...  module=containerd type=io.containerd.grpc.v1
    INFO[0000] loading plugin "io.containerd.monitor.v1.cgroups"...  module=containerd type=io.containerd.monitor.v1
    INFO[0000] loading plugin "io.containerd.runtime.v1.linux"...  module=containerd type=io.containerd.runtime.v1
    INFO[0000] loading plugin "io.containerd.grpc.v1.tasks"...  module=containerd type=io.containerd.grpc.v1
    INFO[0000] loading plugin "io.containerd.grpc.v1.healthcheck"...  module=containerd type=io.containerd.grpc.v1
    INFO[0000] loading plugin "io.containerd.grpc.v1.images"...  module=containerd type=io.containerd.grpc.v1
    INFO[0000] loading plugin "io.containerd.grpc.v1.namespaces"...  module=containerd type=io.containerd.grpc.v1
    INFO[0000] loading plugin "io.containerd.grpc.v1.snapshots"...  module=containerd type=io.containerd.grpc.v1
    INFO[0000] loading plugin "io.containerd.grpc.v1.version"...  module=containerd type=io.containerd.grpc.v1
    INFO[0000] starting GRPC API server...                   module=containerd
    INFO[0000] containerd successfully booted in 0.019407s   module=containerd
    [    2.288861] tsc: Refined TSC clocksource calibration: 3097.775 MHz
    [    2.290004] clocksource: tsc: mask: 0xffffffffffffffff max_cycles: 0x2ca711e180f, max_idle_ns: 440795221899 ns
     - 000-sysctl
    Starting service: "dhcpcd"
    INFO[0000] new shim started                              module="containerd/execution" socket="/var/lib/containerd/io.containerd.runtime.v1.linux/default/dhcpcd/shim.sock"
    Starting service: "getty"
    INFO[0000] new shim started                              module="containerd/execution" socket="/var/lib/containerd/io.containerd.runtime.v1.linux/default/getty/shim.sock"    
    / # Starting service: "rngd"
    INFO[0000] new shim started                              module="containerd/execution" socket="/var/lib/containerd/io.containerd.runtime.v1.linux/default/rngd/shim.sock"
    [    2.533703] IPVS: Creating netns size=2104 id=1
    [    2.533972] IPVS: ftp: loaded support on port[0] = 21
    Starting service: "sshd"
    INFO[0000] new shim started                              module="containerd/execution" socket="/var/lib/containerd/io.containerd.runtime.v1.linux/default/sshd/shim.sock"
    [    3.297574] clocksource: Switched to clocksource tsc
    
    / # uname -a
    Linux linuxkit-025000000004 4.9.32-linuxkit #1 SMP Thu Jun 15 20:49:23 UTC 2017 x86_64 Linux
    / #
    / # halt
    / #

If you watched [Inception](http://www.imdb.com/title/tt1375666/) and didn't have any issues with the different levels of _dreaming_
then the current example with a setup of sshd in a minimal LinuxKit in a hypervised Alpine Linux running on a Mac
is certainly no problem to you...

# LinuxKit on Linode

Ok, let's run the sshd LinuxKit image in a more realistic scenario, namely on a provider like Linode.
I chose Linode because I use it for my personal experiments, but the `sshd.iso` image should run on any KVM based provider.
If you're more into Amazon AWS, you can read a more specific introduction at the [bee42 blog](https://bee42.com/blog/linuxkit-with-initial-aws-support/).

The folks at Linode already have a good article to [get you started with custom images](https://www.linode.com/docs/tools-reference/custom-kernels-distros/install-a-custom-distribution-on-a-linode).
So, all I needed to do was following their instructions - and even skipping some of the described steps, because
the LinuxKit image doesn't need a custom installer like other Linux distributions. So, here's the essence of what you need
to run LinuxKit on a Linode.

Since we would now like to copy our `.iso` image to a Linode disc, we somehow have to provide the image online.
I simply uploaded the `sshd.iso` to another server and temporarily made it available via Nginx:

    local$ scp sshd.iso gesellix@web.example.com:~/nginx-content/sshd.iso
    local$ ssh gesellix@web.example.com
    web$ docker run -d -p 8080:80 -v `pwd`/nginx-content:/usr/share/nginx/html:ro nginx:alpine

Now the `sshd.iso` image is available on the internet and can be downloaded to any server. Let's prepare one.

On Linode, you'll need to create a new disc. The size depends on your needs, obviously, but I chose 1GB as a start.
Then, create a new configuration profile, where all _Filesystem / Boot Helpers_ are disabled and your newly created disc
is mounted to `/dev/sda`. 

Then you'll need to use the rescue mode with your disc being mounted at `/dev/sda`. You can use the _Lish console_
to connect yourself to your Linode. The following commands will download your LinuxKit image and copy its contents
to your empty disc:

    linode/lish$ wget http://web.example.com:8080/sshd.iso
    linode/lish$ dd if=sshd.iso of=/dev/sda

Almost done - you can now close the Lish console and reboot your Linode. After a short while you should be able
to connect to your fresh instance via ssh:

    local$ ssh root@linode.example.com
    Welcome to LinuxKit 
    linuxkit-f23c91e59867:~# 

Linode allows additional optimizations to [increase compatibility](https://www.linode.com/docs/tools-reference/custom-kernels-distros/install-a-custom-distribution-on-a-linode#linode-manager-compatibility) with the Linode manager,
but that's probably a bit too specific for now.

The more interesting part is automation of all the steps above. Linode allows you to use their api and even provide
a [cli tool](https://github.com/linode/cli). As far as I could see they won't allow full automation, yet,
but I'll give it a try at a later time.

Please note that LinuxKit is under heavy development. Usually, the architecture won't change too much, but some
command line options or the image description format might change.

# Feedback

If you have questions or any suggestions, please don't hesitate to contact me via Twitter [@gesellix](https://twitter.com/gesellix)!
Thanks!
