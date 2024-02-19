# Dockerized Django, MySQL, and Nginx Setup

![image](https://github.com/Harasisco/Dockerize_Python_djangoApp/assets/87074807/b15a2d24-d23a-4f7f-bd83-76cb69bfbb72 )

<p>This repository contains a Dockerized setup for running a Django web application with a MySQL database and an Nginx reverse proxy. This setup allows you to easily manage and deploy your Django application in a containerized environment.</p>

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Check The Connectivity](#check-the-connectivity)
- [Compose File](#compose-file)
- [Configuration](#configuration)

## Prerequisites

Make sure you have the following prerequisites installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone this repository to your local machine:

```shell
   git clone https://github.com/Harasisco/Dockarizing-Django-nginx-MySQL.git
   cd Dockarizing-Django-nginx-MySQL
```

2. Create your own docker network:

```shell
  docker network create --subnet=10.0.0.0/24 backend-network
```

3. Build the Django Docker image:

```shell
docker build -t django_image ./django
```

4. Start the MySQL container:

```shell
docker run -d --name db --hostname=MySQL --ip 10.0.0.15  -v ./MySQL/data.sql:/docker-entrypoint-initdb.d/data.sql --net backend-network -e MYSQL_ROOT_PASSWORD=harasisco -e MYSQL_DATABASE=my_database mysql
```

5. Start the Django container:

```shell
docker run -d --name web --hostname=Django_server --ip 10.0.0.10 -v ./django:/code/ --net backend-network --env-file ./django/.env --expose 8000 --link db django_image python3 /code/mysite/manage.py runserver 0.0.0.0:8000
```

6. Start the Nginx container:

```shell
docker run -d --name nginx --hostname=nginx --ip 10.0.0.5  -p 80:80 -v ./nginx/conf.d/:/etc/nginx/conf.d/ --net backend-network --link web nginx:latest 
```

7. Access your Django application in your web browser by navigating to http://localhost or using the IP 127.0.0.1.


## Check The Connectivity

![image](https://github.com/Harasisco/Dockarizing-Django-nginx-MySQL/assets/87074807/84bd4199-694d-4f8a-ab8f-970bbcab51e2)

<p> You can check the network connectivity between nginx and Django by executing the django container and run the **ping** command </p>

```shell
$ docker exec -it <container ID> /bin/bash
```
```shell
root@Django_server:/code# ping nginx
PING nginx_net (10.0.0.5) 56(84) bytes of data.
64 bytes from nginx.backend-network (10.0.0.5): icmp_seq=1 ttl=64 time=0.174 ms
64 bytes from nginx.backend-network (10.0.0.5): icmp_seq=2 ttl=64 time=0.066 ms
64 bytes from nginx.backend-network (10.0.0.5): icmp_seq=3 ttl=64 time=0.261 ms
64 bytes from nginx.backend-network (10.0.0.5): icmp_seq=4 ttl=64 time=0.063 ms
64 bytes from nginx.backend-network (10.0.0.5): icmp_seq=5 ttl=64 time=0.066 ms
64 bytes from nginx.backend-network (10.0.0.5): icmp_seq=6 ttl=64 time=0.066 ms
64 bytes from nginx.backend-network (10.0.0.5): icmp_seq=7 ttl=64 time=0.067 ms
^C
--- nginx_net ping statistics ---
7 packets transmitted, 7 received, 0% packet loss, time 6119ms
rtt min/avg/max/mdev = 0.063/0.109/0.261/0.072 ms

```
### To check the MySQL connectivity:

  - Firstly execute the MySQL container using:
    ```shell
    docker exec -it <container ID>  /bin/bash
    ```
  - Secondery check the MySQL data base info:
    ```shell
    $ mysql -p
    > show databases;
    > use my_database;
    > show tables
    ```
   - You will see that No tables shown.
     
   - In a new tab execute the Django container same as what we did with the MySQL container, then:
     ```shell
     cd mysite/
     python manage.py migrate
     ```
   - Finally, Go back to the MySQL tab and rerun the ``` show tables; ``` command to figoure out that the Django container and MySQL container are linked correctly.

## Compose File

<p> I've included a Docker Compose file (docker-compose.yml) in this project to simplify the setup process and manage the different containers required for our Django application, MySQL database, and Nginx reverse proxy. Docker Compose allows you to define and run multi-container Docker applications with ease.</p>

**Note:** I encountered some errors while using the compose file becouse of depends-on between files that the Django server will not work if the MySQL container not working correctly so I wrote a python script to handle these errors, if You have another solution please tell me.

### To use it Follow these commands:

```shell
docker compose build
docker compose up
```
And when You finsh press ``` Ctrl + C ``` and
```shell
docker compose down
```

## Configuration
- Django settings can be configured in the ./django/mysite/settings.py file.
- MySQL configuration is set in the ./django/.env file under the db service section.
- Nginx configuration files can be added/modified in the ./nginx/conf.d/ directory.
