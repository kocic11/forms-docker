Vagrant.configure("2") do |config|
  (1..3).each do |i|
    config.vm.box = "ubuntu/xenial64"
    config.vm.define "unode-#{i}" do |unode| 
      config.vm.provider "virtualbox" do |vb|
        vb.name = "unode-#{i}"
      end
      unode.vm.network "private_network", ip: "192.168.50.10#{i}"
      unode.vm.provision "shell", path: "bootstrap.sh", env: {"OLD_HOSTNAME" => "ubuntu-xenial", "NEW_HOSTNAME" => "unode#{i}"}
    end
  end
end