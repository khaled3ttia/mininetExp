import mininet.node 
import mininet.link
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import random
import time 

sampleDelays = ['5ms', '10ms', '20ms', '100ms']
sampleLoss = [1, 1.5, 2, 3, 5]
sampleBW = [10, 100, 150, 200, 1000]

# The class where the topology is built
class projectTopo(Topo):

    # This function is called whenever projectTopo() constructor is called
    def build(self):     
        info('Adding hosts\n')
        hosts = []
        switches = []
	
	# We have 10 hosts and 10 switches, starting from id 0 to 9
	# h0 ==> ip: 192.168.1.1 , mac : 00:00:00:00:00:01 , and so on (increments of 1)
        for i in range(10):
	    # The string representing host name, we start from 0 (to allow h0 to h9)
            hostname = 'h' + str(i)

	    # The last octet of ip address for each host is host id + 1
            hostIP = '192.168.1.' + str(i+1)

	    # Same for the mac address
            hostMac = '00:00:00:00:00:0' + str(i+1)

	    # Create the host and add it to the list "hosts"
            hosts.append(self.addHost(hostname, ip=hostIP, mac=hostMac)) 

            # Each host is also connected to a switch of the same id
	    # Create the switch
            switchname = 's' + str(i)
            switches.append(self.addSwitch(switchname))

	    # Add a link between the host and the switch
            self.addLink(hosts[i], switches[i])
        
        info('Creating links\n')

        # The adjacency list used to create other links between different switches
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

	# for each node in the list , iterate over all neighbors and add a link between the node and the neighbor
        for i in range(len(adjList)):
            for j in range(len(adjList[i])):
		# get neighbor id 
                potentialNeighbor = adjList[i][j]

		# Create a set that contains two elements: the node id (i) and the neighbor id (potentialNeighbor)
		# I used a set so that the order does not matter, and a link between two nodes is only added once
		# for example: if we are looking through node 1 neighbors, and found 5 is one of them, we add link between [1,5]
		# 	       then, the adjacency list of node 5 will also contain node 1 as a neighbor, we don't want to add
		#	       the same link again, because this is an undirected graph
                potentialLink = set([i, potentialNeighbor])

		# Only if that set is not in the list of links, add it
                if potentialLink not in links:

		    # I defined the possibilty of introducing link parameters as 25%
                    if (random.random() < 0.25):
                        self.addLink(switches[i], switches[potentialNeighbor], loss=random.choice(sampleLoss), delay=random.choice(sampleDelays), bw=random.choice(sampleBW))
                    else:
                        self.addLink(switches[i], switches[potentialNeighbor])
                    links.append(potentialLink)


	
# The main function that creates and runs the network over Mininet
def createNet():

    # Build topology
    topo = projectTopo()
   
    # create the Mininet object, using the topology, controller, and link
    net = Mininet(topo=topo, controller=RemoteController('c0', ip="10.0.2.15", port=6653), link=TCLink)    

    info('starting network\n')
    net.start()

    info('Running CLI\n')
    CLI(net)

    info('Stopping network')
    net.stop()

# Entry point
if __name__ == '__main__':
    setLogLevel('info')
    createNet()

