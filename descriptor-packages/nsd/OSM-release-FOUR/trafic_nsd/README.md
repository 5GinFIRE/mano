# What is Trafic?

Trafic is an iPerf3 based trafic emulator that allows the creation of traffic flows between two hosts using .yaml configuration files. A more extensive explanation can be found [here](https://github.com/mami-project/trafic).

This NS has all the environment configured and it is ready to be used without any other configuration. The files for the descriptors as well as the Image for the NS can be retrieved [using this link](http://vm-images.netcom.it.uc3m.es/trafic/).

# Network Flow Types

This VNF allows the creation of four different types of traffic flows between two hosts:

1. Greedy: Send a fixed ammount of bytes using maximmum avalaible bandwidth.
2. Scavenger: Send a 30 seconds UDP traffic flow with a fixed bandwidth value.
3. Real-Time audio: A 64Kbps UDP flow with a set duration time (in seconds).
4. Real-Time video: A 330Kbps UDP flow with a set duration time (in seconds).

#Builder

To generate .yaml files to define network flows, this access the /builder directory and run the desired .bash using the following parameters:

-s Server's IP address
-p Port where the server will listen
-b Variable for defining flows

Every flow avalaible is defined by a different parameter. The following network flows with their corresponding defining parameter (-b value meaning) are supported:

1. Greedy: Nº of bytes to be sent.
2. RTA: Duration of the flow in seconds.
3. RTV: Duration of the flow in seconds.
4. Scavenger: Bandwidth used.

The generated flows will be stored under the folder $HOME/webhooks/flows/

If you want to create new .yaml files outside of the provided ones, we recommend following this structure to store the files:

```
$HOME/webhooks/flows/[FLOW_TYPE]/[FLOW_DEFINITION_VARIABLE]/[SERVER_IP]
```

*Make sure both client and server have exactly the same .yaml for running a traffic flow, otherwise it will not work*

#Trafic instantiation

To manage remotely the Trafic tool, we have built-in webhook support. To run this service, it is neccessary to execute the .bash files for the client (run-clients-webhooks.bash) and server (run-servers-webhooks.bash) in the desired hosts. 

Once the webhooks are running, they will listen to HTTP Request petitions. These petitions can be generated using the files under the directory *$HOME/controller/*, where two files will be located (one for the server and another one for the client). 

To execute this files its neccessary to add the following parameters:

-s Server of the traffic flow
-t type of flow (greedy, scavenger, rta, rtv). 
-c defining parameter of the flow (see previous section)
-d destination ip of the request (where the webhook is listening to)

Example:

```
 ./clients.bash -s 10.0.0.1 -t rtv -c 30 -d 10.0.0.4
```

This command will be sent to the client webhook in 10.0.0.4 to run a 30 second real-time audio flow to the server 10.0.0.1, whose descriptor file will be located in $HOME/webhooks/flows/rtv/10.0.0.1/30/. 

In case the request wants to be sent through the command line, use the following format: 

```
curl -d '{"type":"[FLOW_TYPE]", "class":"[CLASS_TYPE]", "label":"[FLOW_SERVER]"}' -H "Content-Type: application/json" -X POST http://[REQUEST_DESTINATION]:9000/hooks/start-[clients/servers]
```

The *clients/servers* option depends on the webhook that wants to be triggered on the receiving end.

This command is equivalent to the previous one for the 30 sec rtv flow:

```
curl -d '{"type":"rtv", "class":"30", "label":"10.0.0.1"}' -H "Content-Type: application/json" -X POST http://10.0.0.4:9000/hooks/start-clients
```

*Important: Run first the server, then the client*
