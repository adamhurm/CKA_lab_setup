CONTROL_PLANES = 3
NODES = 3

UBUNTU_DISTRO = "jammy"
IMAGE_NAME = "ubuntu/#{UBUNTU_DISTRO}64"
KUBERNETES_VERSION = "1.30"
CALICO_VERSION = "3.28.0"

Vagrant.configure("2") do |config|
    config.ssh.insert_key = false

    config.vm.provider "virtualbox" do |v|
        v.memory = 8192
        v.cpus = 2
    end

    # Create HAProxy load balancer if we are using HA configuration
    if CONTROL_PLANES > 1 then 
        config.vm.define "cp-lb" do |cplb|
            cplb.vm.box = IMAGE_NAME
            cplb.vm.network "private_network", ip: "192.168.50.10"
            cplb.vm.hostname = "cp-lb"
            cplb.vm.provision "ha-setup", type:'ansible' do |ansible|
                ansible.compatibility_mode = "2.0"
                ansible.playbook = "ansible/haproxy-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.10",
                    cp_count: CONTROL_PLANES
                }
            end
        end
    end

    # Create control-plane(s)
    (1..CONTROL_PLANES).each do |i|
        config.vm.define "cp-#{i}" do |cp|
            cp.vm.box = IMAGE_NAME
            cp.vm.network "private_network", ip: "192.168.50.#{i + 10}"
            cp.vm.hostname = "cp-#{i}"
            cp.vm.provision "k8s", type:'ansible' do |ansible|
                ansible.compatibility_mode = "2.0"
                ansible.playbook = "ansible/k8s-setup-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.#{i + 10}",
                    k8s_version: KUBERNETES_VERSION,
                    ubuntu_distro: UBUNTU_DISTRO
                }
            end
            # Create one control-plane
            if CONTROL_PLANES == 1 then 
                cp.vm.provision "only-cp", type:'ansible' do |ansible|
                    ansible.compatibility_mode = "2.0"
                    ansible.playbook = "ansible/cp-only-playbook.yml"
                    ansible.extra_vars = {
                        node_ip: "192.168.50.11",
                        node_name: "cp-1",
                        calico_version: CALICO_VERSION
                    }
                end
            # Create multiple control-planes
            else 
                if i == 1 then
                    cp.vm.provision "lead-cp-setup", type:'ansible' do |ansible|
                        ansible.compatibility_mode = "2.0"
                        ansible.playbook = "ansible/cp-lead-playbook.yml"
                        ansible.extra_vars = {
                            node_ip: "192.168.50.11",
                            calico_version: CALICO_VERSION
                        }
                    end
                else
                    cp.vm.provision "ha-cp-setup", type:'ansible' do |ansible|
                        ansible.compatibility_mode = "2.0"
                        ansible.playbook = "ansible/cp-ha-playbook.yml"
                        ansible.extra_vars = {
                            node_ip: "192.168.50.#{i + 10}"
                        }
                    end
                end
            end
        end
    end

    # Create node(s)
    (1..NODES).each do |i|
        config.vm.define "node-#{i}" do |node|
            node.vm.box = IMAGE_NAME
            node.vm.network "private_network", ip: "192.168.50.#{i + 10 + CONTROL_PLANES}"
            node.vm.hostname = "node-#{i}"
            node.vm.provision "k8s", type:'ansible' do |ansible|
                ansible.compatibility_mode = "2.0"
                ansible.playbook = "ansible/k8s-setup-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.#{i + 10 + CONTROL_PLANES}",
                    k8s_version: KUBERNETES_VERSION,
                    ubuntu_distro: UBUNTU_DISTRO
                }
            end
            node.vm.provision "ansible" do |ansible|
                ansible.compatibility_mode = "2.0"
                ansible.playbook = "ansible/node-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.#{i + 10 + CONTROL_PLANES}"
                }
            end
        end
    end
end
