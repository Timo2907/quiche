#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import Intf, TCIntf, TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

from mininet.term import makeTerm, makeTerms
import time
import os.path

def createNetwork():
	#send rate at each link in Mbps
	bwg = 1#000 #1000 #in Mbps
	bwbn = 1#000 #1000 #25 #in Mbps
	loss = 1 #1 #2.5 #10 #1 #in %
	mqs = 100 #0 #1000 #max queue size of interfaces
	dly = '2.5ms'# 0.5ms'#'1ms 0.5ms' #can take all tc qdisc delay distribution formulations

	#create empty network
	net = Mininet(intf=TCIntf)

	info( '\n*** Adding controller\n' )
	net.addController( 'c0' ) #is it ok ?

	#add host to topology
	ht = net.addHost( 'ht', ip='fe80:0:0:0:0:0:a0a:1/64' ) # 10.10.0.1/24 = fe80:0:0:0:0:0:a0a:1 (converted IPv4 to IPv6)
	hu = net.addHost( 'hu', ip='fe80:0:0:0:0:0:a0a:2/64' ) # 10.10.0.2/24 = fe80:0:0:0:0:0:a0a:2
	it = net.addHost( 'it', ip='fe80:0:0:0:0:0:a14:1/64' ) # 10.20.0.1/24 = fe80:0:0:0:0:0:a14:1
	iu = net.addHost( 'iu', ip='fe80:0:0:0:0:0:a14:2/64' ) # 10.20.0.2/24 = fe80:0:0:0:0:0:a14:2

	rh = net.addHost('rh', ip='fe80:0:0:0:0:0:a0a:a/64') # 10.10.0.10/24 = fe80:0:0:0:0:0:a0a:a
	ri = net.addHost('ri', ip='fe80:0:0:0:0:0:a14:14/64') # 10.20.0.20/24 = fe80:0:0:0:0:0:a14:14

	info('\n** Adding Switches\n')
	# Adding 2 switches to the network
	sw1 = net.addSwitch('sw1')
	sw2 = net.addSwitch('sw2')

	info('\n** Creating Links \n')
	#create link beetween the network
	link_ht_sw1 = net.addLink( ht, sw1)
	link_hu_sw1 = net.addLink( hu, sw1)
	link_rh_sw1 = net.addLink( rh, sw1, intfName1='rh-eth0')

	link_it_sw2 = net.addLink( it, sw2)
	link_iu_sw2 = net.addLink( iu, sw2)
	link_ri_sw2 = net.addLink( ri, sw2, intfName1='ri-eth0')

	link_rh_ri  = net.addLink( rh, ri, intfName1='rh-eth1', intfName2='ri-eth1')


	#set bandwith
	link_ht_sw1.intf1.config( bw = bwbn, max_queue_size = mqs)
	link_hu_sw1.intf1.config( bw = bwbn, max_queue_size = mqs)
	link_rh_sw1.intf1.config( bw = bwbn, max_queue_size = mqs) #max_queue_size is hardcoded low to prevent bufferbloat, too high queuing delays

	link_it_sw2.intf1.config( bw = bwg, max_queue_size = mqs)
	link_iu_sw2.intf1.config( bw = bwg, max_queue_size = mqs)
	link_ri_sw2.intf1.config( bw = bwg, max_queue_size = mqs, delay=dly) #delay is set at ri on both interfaces

	link_rh_ri.intf1.config(  bw = bwg, max_queue_size = mqs, loss=loss) #loss is set at rh on its interface to ri only

	link_ht_sw1.intf2.config( bw = bwbn, max_queue_size = mqs)
	link_hu_sw1.intf2.config( bw = bwbn, max_queue_size = mqs)
	link_rh_sw1.intf2.config( bw = bwbn, max_queue_size = mqs)

	link_it_sw2.intf2.config( bw = bwg, max_queue_size = mqs)
	link_iu_sw2.intf2.config( bw = bwg, max_queue_size = mqs)
	link_ri_sw2.intf2.config( bw = bwg, max_queue_size = mqs)

	link_rh_ri.intf2.config(  bw = bwg, max_queue_size = mqs,  delay=dly) #delay is set at ri on both interfaces

	net.start()

	info( '\n*** Configuring hosts\n' )

	rh.cmd('ifconfig rh-eth1 inet6 add fe80:0:0:0:0:0:a0c:a/64')
	rh.cmd('ifconfig rh-eth0 inet6 add fe80:0:0:0:0:0:a0a:a/64')
	rh.cmd('echo 1 > /proc/sys/net/ipv6/conf/all/forwarding')

	ri.cmd('ifconfig ri-eth1 inet6 add fe80:0:0:0:0:0:a0c:14/64')
	ri.cmd('ifconfig ri-eth0 inet6 add fe80:0:0:0:0:0:a14:14/64')
	ri.cmd('echo 1 > /proc/sys/net/ipv6/conf/all/forwarding')

	#configure host default gateways
	ht.cmd('ip -6 route add default via inet6 fe80:0:0:0:0:0:a0a:a dev ht-eth0')
	hu.cmd('ip -6 route add default via inet6 fe80:0:0:0:0:0:a0a:a dev hu-eth0')
	it.cmd('ip -6 route add default via inet6 fe80:0:0:0:0:0:a14:14 dev it-eth0')
	iu.cmd('ip -6 route add default via inet6 fe80:0:0:0:0:0:a14:14 dev iu-eth0')

	#configure router routing tables
	rh.cmd('ip -6 route add default via inet6 fe80:0:0:0:0:0:a0c:14') # NOT WORKING (Invalid argument) -> check ip -6 route help
	ri.cmd('ip -6 route add default via inet6 fe80:0:0:0:0:0:a0c:a') # NOT WORKING

        # weiyu:
        iu.cmd('touch server.pcap')
        hu.cmd('touch client.pcap')


        rh.cmd('tc qdisc del dev rh-eth1 root')
	
	#TODO for experiment setup: comment in
	# start_nodes(rh, ri, iu, hu, mqs) #experiment actions


	it.cmd('ethtool -K it-eth0 tx off sg off tso off') #disable TSO on TCP on defaul TCP sender need to be done on other host if sending large TCP file from other nodes

	time.sleep(1)

	# Enable the mininet> prompt if uncommented
	info('\n*** Running CLI\n')
	CLI(net)

	# stops the simulation
	net.stop()

def start_nodes(delay_router, loss_router, server, client, mqs):

 delay_router.cmd('tc qdisc add dev rh-eth1 root netem loss gemodel 1.11% 10% 100% 0% limit ' + str(mqs))
 #move-to-burstmode (p) of 1.11%, move-to-gapmode (r) of 10%, drop-in-burstmode (1-h) of 100% and drop-in-gapmode (1-k) of 0%

 #delay_router.cmd('sudo python ./monitor_queue.py &')
 #loss_router.cmd('python ./monitor_qlen_ri.py &')
 #info( '\n*** Set up of in-network routers completed.\n' )

 server.cmd('tshark -i iu-eth0 -w server.pcap &')
 server.cmd('sudo ./start_quiche_server.sh > output-server.txt &')
 info( '\n*** QUICHE Server started...\n' )

 client.cmd('tshark -i hu-eth0 -w client.pcap &')
 client.cmd('sleep 5; sudo ./start_quiche_client.sh > output-client.txt &')
 info( '\n*** QUICH Client started...\n' )


if __name__ == '__main__':
	setLogLevel( 'info' )
	#setLogLevel( 'output' )
	createNetwork()
