# Cloud Provider

Implementing a bare metal cloud computing provider system with ```python```, ```rabbitmq```, and ```qemu```.
My goal is to create an on-demand computing platform like EC2 (aka Amazon Elastic Compute Cloud).
This provider is capable of:

- spin up ```VMs``` on-demand
- take down ```VMs``` on-demand
- allow to use or not use a public IP on a ```VM```
- be scalable in the background, i.e. possibly ```VMs``` are on different servers
