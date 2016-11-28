import random
import string
import os
import inspect

from shutit_module import ShutItModule

class shutit_docker_distribution(ShutItModule):


	def build(self, shutit):
		vagrant_image = shutit.cfg[self.module_id]['vagrant_image']
		vagrant_provider = shutit.cfg[self.module_id]['vagrant_provider']
		gui = shutit.cfg[self.module_id]['gui']
		memory = shutit.cfg[self.module_id]['memory']
		run_dir = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))) + '/vagrant_run'
		module_name = 'shutit_docker_distribution_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
		shutit.send('command rm -rf ' + run_dir + '/' + module_name + ' && command mkdir -p ' + run_dir + '/' + module_name + ' && command cd ' + run_dir + '/' + module_name)
		if shutit.send_and_get_output('vagrant plugin list | grep landrush') == '':
			shutit.send('vagrant plugin install landrush')
		shutit.send('vagrant init ' + vagrant_image)
		shutit.send_file(run_dir + '/' + module_name + '/Vagrantfile','''Vagrant.configure("2") do |config|
  config.landrush.enabled = true
  config.vm.provider "virtualbox" do |vb|
    vb.gui = ''' + gui + '''
    vb.memory = "''' + memory + '''"
  end

  config.vm.define "distributionserver" do |distributionserver|
    distributionserver.vm.box = ''' + '"' + vagrant_image + '"' + '''
    distributionserver.vm.hostname = "distributionserver.vagrant.test"
  end

  config.vm.define "client1" do |client1|
    client1.vm.box = ''' + '"' + vagrant_image + '"' + '''
    client1.vm.hostname = "client1.vagrant.test"
  end
end''')
		pw = shutit.get_env_pass()
		try:
			shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'],{'assword for':pw},timeout=99999)
		except:
			shutit.multisend('vagrant up',{'assword for':pw},timeout=99999)
		distributionserver_ip = shutit.send_and_get_output('''vagrant landrush ls | grep -w ^distributionserver.vagrant.test | awk '{print $2}' ''')
		client1_ip = shutit.send_and_get_output('''vagrant landrush ls | grep -w ^client1.vagrant.test | awk '{print $2}' ''')
		shutit.login(command='vagrant ssh distributionserver')
		shutit.login(command='sudo su -',password='vagrant')

		shutit.pause_point('')

		shutit.logout()
		shutit.logout()
		return True

	def get_config(self, shutit):
		shutit.get_config(self.module_id,'vagrant_image',default='centos/7')
		shutit.get_config(self.module_id,'vagrant_provider',default='virtualbox')
		shutit.get_config(self.module_id,'gui',default='false')
		shutit.get_config(self.module_id,'memory',default='512')

		return True

	def test(self, shutit):

		return True

	def finalize(self, shutit):

		return True

	def isinstalled(self, shutit):

		return False

	def start(self, shutit):

		return True

	def stop(self, shutit):

		return True

def module():
	return shutit_docker_distribution(
		'imiell.shutit_docker_distribution.shutit_docker_distribution', 53766448.0001,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup','shutit-library.virtualbox.virtualbox.virtualbox','tk.shutit.vagrant.vagrant.vagrant']
	)
