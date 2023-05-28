# CKA Lab Setup

## Quickstart

Install the following:
- [vagrant](https://developer.hashicorp.com/vagrant/downloads)
- [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads)
- [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

```shell
$ git clone git@github.com:adamhurm/CKA_lab_setup.git
$ cd CKA_lab_setup
$ vagrant up
```


Now log into the HAProxy VM and uncomment the lines to start load balancing:

```shell
$ vagrant ssh cplb
$ sudo -e /etc/haproxy/haproxy.cfg

### /etc/haproxy/haproxy.cfg
...
backend k8sServers
   balance roundrobin
   server cp0  192.168.50.10:6443 check
#   server cp1  192.168.50.11:6443 check <--uncomment for each additional control-plane
#   server cp2  192.168.50.12:6443 check <--uncomment for each additional control-plane
...
===>
...
backend k8sServers
   balance roundrobin
   server cp0  192.168.50.10:6443 check
   server cp1  192.168.50.11:6443 check
   server cp2  192.168.50.12:6443 check
...

$ sudo systemctl restart haproxy
```


## Customize

Launch high availability cluster. This HA cluster will use [stacked etcd](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/ha-topology/#stacked-etcd-topology). The following will create C+1 control-planes, N nodes, and 1 load balancer.

ℹ️ If you increase the number of control-planes, make sure to create a new line for the new control-plane(s) in haproxy.cfg

```Vagrantfile
### Vagrantfile
...
C = 2  # additional control-planes
N = 3  # nodes
...
v.memory = 8192
v.cpus = 3
```

## High Availability

Introduced later in the lab. I will clean this code up soon so that you can use original or HA in the Vagrantfile. I will also take a look at automating the /etc/haproxy/haproxy.cfg file modification.


## References

Vagrantfile template taken from [this Kubernetes blog post](https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/). Updated for 22.04 LTS (Focal Fossa).

High Availability guidance taken from these kubernetes documentation pages: [kubeadm create cluster](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/), [kubeadm high availbility](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/), [kubeadm setup ha etcd](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/)