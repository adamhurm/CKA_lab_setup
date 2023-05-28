IMAGE_NAME = "ubuntu/focal64"
C = 1
N = 3

Vagrant.configure("2") do |config|
    config.ssh.insert_key = false

    config.vm.provider "virtualbox" do |v|
        v.memory = 8192
        v.cpus = 2
    end

    if C > 1 then
        config.vm.define "cp-lb" do |cplb|
            cplb.vm.box = IMAGE_NAME
            cplb.vm.network "private_network", ip: "192.168.50.10"
            cplb.vm.hostname = "cp-lb"
            cplb.vm.provision "ansible" do |ansible|
                ansible.compatibility_mode = "2.0"
                ansible.playbook = "kubernetes-setup/haproxy-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.10",
                }
            end
        end
    end

    (1..C).each do |i|
        config.vm.define "cp-#{i}" do |cp|
            cp.vm.box = IMAGE_NAME
            cp.vm.network "private_network", ip: "192.168.50.#{i + 10}"
            cp.vm.hostname = "cp-#{i}"
            cp.vm.provision "k8s", type:'ansible' do |ansible|
                ansible.compatibility_mode = "2.0"
                ansible.playbook = "kubernetes-setup/k8s-setup-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.#{i + 10}",
                }
            end
            if C == 1 then
                cp.vm.provision "only-cp", type:'ansible' do |ansible|
                    ansible.compatibility_mode = "2.0"
                    ansible.playbook = "kubernetes-setup/cp-only-playbook.yml"
                    ansible.extra_vars = {
                        node_ip: "192.168.50.10",
                    }
                end
            else 
                if i == 1 then
                    cp.vm.provision "lead-cp-setup", type:'ansible' do |ansible|
                        ansible.compatibility_mode = "2.0"
                        ansible.playbook = "kubernetes-setup/cp-lead-playbook.yml"
                        ansible.extra_vars = {
                            node_ip: "192.168.50.#{i + 10}",
                        }
                    end
                else
                    cp.vm.provision "ha-cp-setup", type:'ansible' do |ansible|
                        ansible.compatibility_mode = "2.0"
                        ansible.playbook = "kubernetes-setup/cp-ha-playbook.yml"
                        ansible.extra_vars = {
                            node_ip: "192.168.50.#{i + 10}",
                        }
                    end
                end
            end
        end
    end

    (1..N).each do |i|
        config.vm.define "node-#{i}" do |node|
            node.vm.box = IMAGE_NAME
            node.vm.network "private_network", ip: "192.168.50.#{i + 10 + C}"
            node.vm.hostname = "node-#{i}"
            node.vm.provision "k8s", type:'ansible' do |ansible|
                ansible.compatibility_mode = "2.0"
                ansible.playbook = "kubernetes-setup/k8s-setup-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.#{i + 10 + C}",
                }
            end
            node.vm.provision "ansible" do |ansible|
                ansible.compatibility_mode = "2.0"
                ansible.playbook = "kubernetes-setup/node-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.#{i + 10 + C}",
                }
            end
        end
    end
end
