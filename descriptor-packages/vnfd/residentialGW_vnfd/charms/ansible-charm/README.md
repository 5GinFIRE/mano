# Overview
This base charm layer provides a template to create a *proxy charm*, which enables to configure a Virtual Network Function (VNF) instantiated trough Open Source MANO (OSM) using an Ansible playbook. The files included in this charm layer are free to use under the terms provided by the license information specified below.


# Usage
The base charm layer includes the following base layers: [vnfproxy](https://github.com/AdamIsrael/vnfproxy) and [ansible-base](https://github.com/chuckbutler/ansible-base). It provides a template ready for customization, which enables to create a *proxy charm* that supports the execution of an Ansible playbook to configure a VNF. For more information on *proxy charms*, the reader is referred to the [OSM wiki](https://osm.etsi.org/wikipub/index.php/Creating_your_own_VNF_charm_(Release_TWO)).

Step by step instructions to use the base charm layer:

1. Include the playbook under the *playbook* folder of the base charm layer; name it as *playbook.yaml*. Alternatively, you can open the file *playbook.yaml* alreay existing in this directory and paste the playbook in this file.

2. The base charm layer already implements a Juju action, _**ansible-playbook**_, which runs the playbook *playbook/playbook.yaml*. You can optionally define additional actions, if needed by your VNF.

3. Build the charm, via the *charm build* command.

4. Update the VNF descriptor (VNFD) to use the charm: a) specify the name of the Juju charm in in the VNF configuration; b) Include the action “ansible-playbook” with no arguments as a service primitive and as an initial configuration primitive.

5. Include the compiled charm in the VNF package.

More comprehensive and complementary information on building *Proxy charms* can be found in the [OSM wiki](https://osm.etsi.org/wikipub/index.php/Creating_your_own_VNF_charm_(Release_TWO)) and in the documentation of the [vnfproxy layer](https://github.com/AdamIsrael/vnfproxy).

# Contact Information
Borja Nogales Dorado <bdorado@pa.uc3m.es>.  
Universidad Carlos III de Madrid (www.uc3m.es).

# Upstream Project Name
This work has been supported by the European H2020 5GinFIRE project (grant agreement 732497).

# License
Copyright 2017 Borja Nogales <bdorado@pa.uc3m.es>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


