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
Once the HAProxy (**cp-lb**) playbook finishes, you can view the HAProxy status page here: http://192.168.50.10:9999/stats/

[This script](ansible/scripts/ping-and-update.sh) will run on **cp-lb** to watch control-planes and [add them](ansible/scripts/update-haproxy-cfg.py) to HAProxy config as they come online.

```bash
$ vagrant ssh cp-1
vagrant@cp-1:~$ kubectl get node
NAME     STATUS   ROLES           AGE   VERSION
cp-1     Ready    control-plane   86m   v1.27.2
cp-2     Ready    control-plane   84m   v1.27.2
cp-3     Ready    control-plane   81m   v1.27.2
node-1   Ready    <none>          79m   v1.27.2
node-2   Ready    <none>          77m   v1.27.2
node-3   Ready    <none>          75m   v1.27.2
```

<br>

## Customize

### High Availability

By default, creates high availability cluster with [stacked etcd](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/ha-topology/#stacked-etcd-topology). 

The following suggested config will use:
- 3 control-planes
- 3 nodes
- 1 load balancer (always)
- Total: 14 vCPUs, 56GB RAM

To change this behavior, edit the following values in Vagrantfile:
```Vagrantfile
### Vagrantfile
...
C = 3  # control-planes
N = 3  # nodes
...
v.memory = 8192
v.cpus = 2
```

<br>

### Single Control-Plane
You can also create clusters with only one control-plane.

Edit the following values in Vagrantfile to create 1 control-plane and 2 nodes:
```Vagrantfile
### Vagrantfile
...
C = 1 # control-plane
N = 2 # nodes
...
# allocate 2 vCPUs and 8GB RAM to each VM
v.memory = 8192
v.cpus = 2
```

<br>


## To-do

 - Automate certificate deletion. (token expires after 2 hours but this isn't ideal to leave on disk)


## References

Vagrantfile template taken from [this Kubernetes blog post](https://kubernetes.io/blog/2019/03/15/kubernetes-setup-using-ansible-and-vagrant/). Updated for 22.04 LTS (Focal Fossa).

High Availability guidance taken from these kubernetes documentation pages: [kubeadm create cluster](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/), [kubeadm high availbility](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/), [kubeadm setup ha etcd](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/)