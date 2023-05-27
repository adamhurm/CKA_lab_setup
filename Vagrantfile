IMAGE_NAME = "ubuntu/focal64"
C = 2
N = 3

Vagrant.configure("2") do |config|
    config.ssh.insert_key = false

    config.vm.provider "virtualbox" do |v|
        v.memory = 8192
        v.cpus = 3
    end

    config.vm.define "cplb" do |cplb|
        cplb.vm.box = IMAGE_NAME
        cplb.vm.network "private_network", ip: "192.168.50.9"
        cplb.vm.hostname = "cplb"
        cplb.vm.provision "ansible" do |ansible|
            ansible.playbook = "kubernetes-setup/proxy-playbook.yml"
            ansible.extra_vars = {
                node_ip: "192.168.50.9",
            }
        end
    end

    config.vm.define "cp0" do |master|
        master.vm.box = IMAGE_NAME
        master.vm.network "private_network", ip: "192.168.50.10"
        master.vm.hostname = "cp0"
        master.vm.provision "ansible" do |ansible|
            ansible.compatibility_mode = "2.0"
            ansible.playbook = "kubernetes-setup/master-playbook.yml"
            ansible.extra_vars = {
                node_ip: "192.168.50.10",
            }
        end
    end

    (1..C).each do |i|
        config.vm.define "cp#{i}" do |cp|
            cp.vm.box = IMAGE_NAME
            cp.vm.network "private_network", ip: "192.168.50.#{i + 10}"
            cp.vm.hostname = "cp#{i}"
            cp.vm.provision "ansible" do |ansible|
                ansible.compatibility_mode = "2.0"
                ansible.playbook = "kubernetes-setup/ha-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.#{i + 10}",
                }
            end
        end
    end

    (1..N).each do |i|
        config.vm.define "node#{i}" do |node|
            node.vm.box = IMAGE_NAME
            node.vm.network "private_network", ip: "192.168.50.#{i + 10 + C}"
            node.vm.hostname = "node#{i}"
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
