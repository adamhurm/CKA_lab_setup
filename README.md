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


## Customize

### Single Control Plane
By default, creates one control-plane and two nodes. Allocates 3 vCPUs and 8GB to each VM.

To change this behavior, edit the following values in Vagrantfile:
```Vagrantfile
### Vagrantfile
...
C = 1 # control-plane
N = 2 # nodes
...
v.memory = 8192
v.cpus = 3
```


### High Availability

Launch high availability cluster. This HA cluster will use [stacked etcd](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/ha-topology/#stacked-etcd-topology). So this default will create 3 control-planes, 3 nodes, and 1 load balancer which will consume 56GB RAM and 21 CPU cores.

ℹ️ If you increase the number of control-planes, make sure to create a new line for the new control-plane(s) in haproxy.cfg

```Vagrantfile
### Vagrantfile
...
C = 3  # control-planes
N = 3  # nodes
...
v.memory = 8192
v.cpus = 3
```

```shell
$ git clone git@github.com:adamhurm/CKA_lab_setup.git
$ cd CKA_lab_setup
$ vagrant up
```

You can now view load balancer status here: http://192.168.50.10:9999/stats/


## To-do

 - Automate certificate deletion. (token expires after 2 hours but this isn't ideal to leave on disk)


## References

Vagrantfile template taken from [this Kubernetes blog post](https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/). Updated for 22.04 LTS (Focal Fossa).

High Availability guidance taken from these kubernetes documentation pages: [kubeadm create cluster](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/), [kubeadm high availbility](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/), [kubeadm setup ha etcd](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/)