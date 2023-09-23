# Cloud Provider

Implementing a bare metal cloud computing provider system with ```python```, ```rabbitmq```, and ```qemu```.
My goal is to create an on-demand computing platform like EC2 (aka Amazon Elastic Compute Cloud).
This provider is capable of:

- Spin up ```VM```s on-demand
- Take down ```VM```s on-demand
- Allow to use or not use a public IP on a ```VM```
- Be scalable in the background, i.e. possibly ```VM```s are on different servers
