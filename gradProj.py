from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import random
import time 

class projectTopo(Topo):
    def build(self):
        
        info('Adding hosts\n')
        hosts = []
        switches = []
        for i in range(10):
            hostname = 'h' + str(i)
            hostIP = '192.168.1.' + str(i+1)
            hostMac = '00:00:00:00:00:0' + str(i+1)
            hosts.append(self.addHost(hostname, ip=hostIP, mac=hostMac)) 
            switchname = 's' + str(i)
            switches.append(self.addSwitch(switchname))
            self.addLink(hosts[i], switches[i])
        
        info('Creating links\n')
        adjList = [[1, 2, 8],
               [0, 2, 3, 9],
               [0, 1, 4, 5, 7],
               [1, 4, 9],
               [2, 3, 5, 9],
               [2, 4, 6, 8, 9],
                   [5, 7],
                   [2, 6, 8],
               [0, 5, 7],
               [1, 3, 4, 5]]
        
        links = []

        for i in range(len(adjList)):
            for j in range(len(adjList[i])):
                potentialNeighbor = adjList[i][j]
                potentialLink = set([i, potentialNeighbor])
                if potentialLink not in links:
                    if (random.random() < 0.25):
                        sampleDelays = ['5ms', '10ms', '20ms', '100ms']
                        sampleLoss = [1, 1.5, 2, 3, 5]
                        sampleBW = [10, 100, 150, 200, 1000]
                        self.addLink(switches[i], switches[potentialNeighbor], loss=2, delay='5ms', bw=10)
                    else:
                        self.addLink(switches[i], switches[potentialNeighbor])
                    links.append(potentialLink)


	

def emptyNet():
    topo = projectTopo()
    net = Mininet(topo=topo, controller=RemoteController, link=TCLink)
    info('Adding Controller\n')
    net.addController('c0', controller=RemoteController, ip="10.0.2.15", port=6653)

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
