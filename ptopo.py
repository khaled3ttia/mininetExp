from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time 
def emptyNet():
    net = Mininet(controller=RemoteController)
    info('Adding Controller\n')
    net.addController('c0', controller=RemoteController, ip="10.0.2.15", port=6653)

    info('Adding hosts\n')
    h1 = net.addHost('h1', ip="10.0.0.1")
    h2 = net.addHost('h2', ip="10.0.0.2")

    info('Adding Swithes\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    info('Creating Links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s3)

    SwitchList = (s1, s2, s3, s4)
    for index in range(0, len(SwitchList)):
	for index2 in range(index+1, len(SwitchList)):
	    net.addLink(SwitchList[index], SwitchList[index2])

    info('starting network\n')
    net.start()

    info('Running CLI\n')
    CLI(net)

    info('Stopping network')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    emptyNet()

'''
class MyTopo(Topo):


    def __init__(self):
	#Initialize Topology
        Topo.__init__(self)
	
	#Add hosts and switches
	leftHost = self.addHost('h1')
	rightHost = self.addHost('h2')
	leftSwitch = self.addSwitch('s1')
	rightSwitch = self.addSwitch('s2')

	# Add links
	self.addLink(leftHost, leftSwitch)
	self.addLink(leftSwitch, rightSwitch)
	self.addLink(rightSwitch, rightHost)

topos = {'mytopo': (lambda: MyTopo())}
'''
