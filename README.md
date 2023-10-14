# Cloud Provider

![GitHub top language](https://img.shields.io/github/languages/top/amirhnajafiz/cloud-provider)
![GitHub release (with filter)](https://img.shields.io/github/v/release/amirhnajafiz/cloud-provider)

Implementing a bare metal cloud computing provider system with ```python```, ```rabbitmq```, and ```qemu```.
My goal is to create an on-demand computing platform like EC2 (aka Amazon Elastic Compute Cloud).
This provider is capable of:

- Spin up ```VM```s on-demand
- Take down ```VM```s on-demand
- Allow to use or not use a public IP on a ```VM```
- Be scalable in the background, i.e. possibly ```VM```s are on different servers

## Schema

In the following textbox we are displaying our cloud provider schema. As the image states,
first the user sends a request into rabbitMQ cluster to perform an operation. On the other side,
the consumer is bound to listen for user requests. After receiving each request, consumer
checks the input request and calls fallback functions.

```
| make publish | -> | consume by consumer | -> | callback function based on request |
```

### commands

In the following list you can see ```CLI``` commands:

- ```start-vm --image [image name]```
- ```list-vm```
- ```stop-vm --vm-id [id returned in list-vm]```
