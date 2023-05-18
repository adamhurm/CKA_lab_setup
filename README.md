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

By default, creates one control-plane and two nodes. Allocates 3 vCPUs and 8GB to each VM.

To change this behavior, edit the following values in Vagrantfile:
```
# Vagrantfile
...
N = 2
...
v.memory = 8192
v.cpus = 3
```


## References

Vagrantfile template taken from [this Kubernetes blog post](https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/). Updated for 22.04 LTS (Focal Fossa).