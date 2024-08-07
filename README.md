# CKA Lab Setup

Create a high availability cluster with [stacked etcd](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/ha-topology/#stacked-etcd-topology).

The default configuration is:
- 3 control-planes
- 3 nodes
- 1 load balancer
- Total: 14 vCPUs, 56GB RAM

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

```shell
$ vagrant ssh cp-1
vagrant@cp-1:~$ kubectl get node -o wide
NAME     STATUS   ROLES           AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
cp-1     Ready    control-plane   32m   v1.30.2   192.168.50.11   <none>        Ubuntu 22.04.4 LTS   5.15.0-113-generic   containerd://1.7.18
cp-2     Ready    control-plane   30m   v1.30.2   192.168.50.12   <none>        Ubuntu 22.04.4 LTS   5.15.0-113-generic   containerd://1.7.18
cp-3     Ready    control-plane   26m   v1.30.2   192.168.50.13   <none>        Ubuntu 22.04.4 LTS   5.15.0-113-generic   containerd://1.7.18
node-1   Ready    <none>          24m   v1.30.2   192.168.50.14   <none>        Ubuntu 22.04.4 LTS   5.15.0-113-generic   containerd://1.7.18
node-2   Ready    <none>          23m   v1.30.2   192.168.50.15   <none>        Ubuntu 22.04.4 LTS   5.15.0-113-generic   containerd://1.7.18
node-3   Ready    <none>          21m   v1.30.2   192.168.50.16   <none>        Ubuntu 22.04.4 LTS   5.15.0-113-generic   containerd://1.7.18
```
Once the HAProxy (**cp-lb**) playbook finishes, you can view the HAProxy status page: http://192.168.50.10:9999/stats/

[This script](ansible/scripts/ping-and-update.sh) will run on **cp-lb** to watch control-planes and [add them](ansible/scripts/update-haproxy-cfg.py) to HAProxy config as they come online.


## Customize

### High Availability
The following suggested config will use 3 control-planes, 3 nodes, 1 load balancer (always). Total: 14 vCPUs, 56GB RAM

To change this behavior, edit the following values in [Vagrantfile](./Vagrantfile):
```Vagrantfile
...
CONTROL_PLANES = 3  # >1 creates a load balancer (cp-lb)
NODES = 3
...
v.memory = 8192
v.cpus = 2
```


### Single Control-Plane
You can also create clusters with only one control-plane.

Edit the following values in [Vagrantfile](./Vagrantfile) to create 1 control-plane and 2 nodes:
```Vagrantfile
...
CONTROL_PLANES = 1
NODES = 2
...
# allocate 2 vCPUs and 8GB RAM to each VM
v.memory = 8192
v.cpus = 2
```

<br>


## To-do

 - Automate certificate deletion. (token expires after 2 hours but this isn't ideal to leave on disk)


## References

Vagrantfile template taken from [this Kubernetes blog post](https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/). Updated for Ubuntu 22.04 LTS (Jammy Jellyfish).

High Availability guidance taken from these kubernetes documentation pages: [kubeadm create cluster](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/), [kubeadm high availbility](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/), [kubeadm setup ha etcd](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/)
