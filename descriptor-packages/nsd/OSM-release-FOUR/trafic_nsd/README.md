# What is Trafic?

Trafic is an iPerf3 based trafic emulator that allows the creation of traffic flows between two hosts using .yaml configuration files. A more extensive explanation can be found [here](https://github.com/mami-project/trafic).

This NS has all the environment configured and it is ready to be used without any other configuration. The files for the descriptors as well as the Image for the NS can be retrieved [using this link](http://vm-images.netcom.it.uc3m.es/trafic/).

# Network Flow Types

This VNF allows the creation of four different types of traffic flows between two hosts:

1. Greedy: Send a fixed ammount of bytes using a TCP flow with maximmum avalaible bandwidth.
2. Scavenger: Send a 30 seconds UDP traffic flow with a fixed bandwidth value.
3. Real-Time audio: A 64Kbps UDP flow with a set duration time (in seconds).
4. Real-Time video: A 330Kbps UDP flow with a set duration time (in seconds).

# Builder

To generate .yaml files to define network flows, access the _/builder_ directory and run the desired .bash using the following parameters:

* -s Server's IP address
* -p Port where the server will listen
* -b Variable for defining flows

Every flow avalaible is defined by a different parameter. The following network flows with their corresponding defining parameter _(-b value meaning)_ are supported:

1. Greedy: Nº of bytes to be sent
2. RTA: Duration of the flow in seconds
3. RTV: Duration of the flow in seconds
4. Scavenger: Bandwidth used

The generated flows will be stored under the folder _$HOME/webhooks/flows/_

If you want to create new .yaml files outside of the provided ones, we recommend following this structure to store the files:

```
$HOME/webhooks/flows/[FLOW_TYPE]/[FLOW_DEFINITION_VARIABLE]/[SERVER_IP]
```

Example: Generating a greedy TCP flow to send 500M with server 10.0.0.1 in port 5057

```
./greedy.bash -s 10.0.0.1 -p 5057 -b 500M
```

The generated file will be located at the directory _$HOME/webhooks/flows/greedy/10.0.0.1/_ 

**Make sure both client and server have exactly the same .yaml for running a traffic flow, otherwise it will not work**

# Trafic instantiation

To manage remotely the Trafic tool, we have built-in webhook support. To run them, it is neccessary to execute the .bash file for the server and client in the desired hosts (the file allows both modes at the same time). We reccomend executing this command in a separated terminal (using the _screen_ program, for example). The executed command should look like this:

```
./run-hooks.bash
```

Once the webhooks are running, they will listen to HTTP Request petitions. These petitions can be generated using the files under the directory *$HOME/controller/*, where two files will be located (one for the server and another one for the client). 

To execute this files its neccessary to add the following parameters:

* -s Server of the traffic flow
* -t type of flow (greedy, scavenger, rta, rtv) 
* -c defining parameter of the flow (see previous section)
* -d destination ip of the request (where the webhook is listening to)
* -n InfluxDB measurement name in a database (used only for the client)

Example:

```
./servers.bash -s 10.0.0.1 -t rtv -c 30 -d 10.0.0.1
./clients.bash -s 10.0.0.1 -t rtv -c 30 -d 10.0.0.4 -n MEASUREMENT_EXAMPLE
```

The first command will be sent to the server webhook in 10.0.0.1 to run a 30 second real-time audio flow to the server 10.0.0.1, whose descriptor file will be located in _$HOME/webhooks/flows/rtv/10.0.0.1/30/_.
The second command will be sent to the client webhook in 10.0.0.4 to run a 30 second real-time audio flow to the server 10.0.0.1, whose descriptor file will be located in _$HOME/webhooks/flows/rtv/10.0.0.1/30/_. The results will be dropped in the MEASUREMENT_EXAMPLE table in the destination InfluxDB (see Database support section). 

In case the request wants to be sent through the command line, use the following format: 

```
curl -d '{"type":"[FLOW_TYPE]", "class":"[CLASS_TYPE]", "label":"[FLOW_SERVER]", "name":"[INFLUXDB_MEASUREMENT]"}' -H "Content-Type: application/json" -X POST http://[REQUEST_DESTINATION]:9000/hooks/start-[clients/servers]
```

The *clients/servers* option depends on the webhook that wants to be triggered on the receiving end.

This command is equivalent to the previous one for the 30 sec rtv flow:

```
curl -d '{"type":"rtv", "class":"30", "label":"10.0.0.1", "name":"MEASUREMENT_EXAMPLE"}' -H "Content-Type: application/json" -X POST http://10.0.0.4:9000/hooks/start-clients
```

**Important: Run first the server, then the client**

# Database Support

Trafic allows to store iperf3 flow statistics in a remote _InfluxDB_ database. To do so, modify the variables DATABASE and INFLUXDB with the database name and its ip address respectively inside the file run-clients.bash in the directory _$HOME/webhooks/_.
