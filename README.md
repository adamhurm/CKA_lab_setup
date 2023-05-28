# CKA Lab Setup

## Quickstart

Install the following:
- [vagrant](https://developer.hashicorp.com/vagrant/downloads)
- [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads)
- [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

```
$ git clone git@github.com:adamhurm/CKA_lab_setup.git
$ cd CKA_lab_setup
$ vagrant up
```


## Customize

Launch high availability cluster. This HA cluster will use [stacked etcd](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/ha-topology/#stacked-etcd-topology).

```
# Vagrantfile
...
C = 2  # additional control-planes
N = 3  # nodes
...
v.memory = 8192
v.cpus = 3
```


## References

Vagrantfile template taken from [this Kubernetes blog post](https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/). Updated for 22.04 LTS (Focal Fossa).

High Availability guidance taken from these kubernetes documentation pages: [kubeadm create cluster](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/), [kubeadm high availbility](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/), [kubeadm setup ha etcd](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/)