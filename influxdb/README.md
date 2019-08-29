# Dummy sensor (influxdb)

This dummy sensor writes to an influxdb database, and is used to demonstrate a possible IOT pipeline with three services: 

* the said sensor
* an influxdb server
* a grafana server for display

## Settting up the stack

The stack was tested on a mac with Docker Desktop (amd64 architecture), and on a raspberry pi 3B+ (armv71 architecture). 

There were two slight issues in setting up these stacks: 

* grafana does not work on arm
* on the raspberri pi, the docker compose version v3 is not supported (at least in my install of docker). 

Therefore, I provide two different `docker-compose.yml` files, one for each architecture: 

[amd64](https://github.com/cbernet/maldives/blob/master/influxdb/docker-compose.yml): 

* docker-compose version 3
* official [grafana container](https://hub.docker.com/r/grafana/grafana)

[armv71](https://github.com/cbernet/maldives/blob/rpi_docker/influxdb/docker-compose.yml)

* docker-compose version 2 
* unofficial [grafana container for arm by proxx](https://hub.docker.com/r/proxx/grafana-armv7) (thanks!)

Download the one you need, and do: 

```
docker-compose up 
```

to start the stack.
 

## Visualizing the data

The dummy sensor in this image generates a point on a sine wave every s and stores it in the influx db database. 

Point your browser to [http://localhost:3000]() 

Log in to grafana with the default username and password (admin/admin), and configure your dashboard to read from influxdb. 
