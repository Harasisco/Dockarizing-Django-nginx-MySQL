# Dockerized Django, MySQL, and Nginx Setup

This repository contains a Dockerized setup for running a Django web application with a MySQL database and an Nginx reverse proxy. This setup allows you to easily manage and deploy your Django application in a containerized environment.

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
  docker network create <Name of the network>  ## I will call it test
```

3. Build the Django Docker image:

```shell
docker build -t django_image ./django
```

4. Start the MySQL container:

```shell
docker run -d --name db -v ./MySQL/data.sql:/docker-entrypoint-initdb.d/data.sql --net test -e MYSQL_ROOT_PASSWORD=harasisco -e MYSQL_DATABASE=my_database mysql
```

5. Start the Django container:

```shell
docker run -d --name web -v ./django:/code/ --net test --env-file ./django/.env --expose 8000 --link db django_image python3 /code/mysite/manage.py runserver 0.0.0.0:8000
```

6. Start the Nginx container:

```shell
docker run -d --name nginx -p 80:80 -v ./nginx/conf.d/:/etc/nginx/conf.d/ --net test --link web nginx:latest 
```

7. Access your Django application in your web browser to check the server type by navigating to http://localhost or using the IP 127.0.0.1.

![image](https://github.com/Harasisco/Dockarizing-Django-nginx-MySQL/assets/87074807/84bd4199-694d-4f8a-ab8f-970bbcab51e2)

8. To check the MySQL connectivity:

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
     
   - In a new tab execute the Django container same as the MySQL container, then:
     ```shell
     cd mysite/
     python manage.py migrate
     ```
   - Finally, Go back to the MySQL tab and rerun the ``` show tables; ``` command to figoure out that the Django container and MySQL container are linked correctly.

##Configuration
- Django settings can be configured in the /django/mysite/settings.py file.
- MySQL configuration is set in the /django/.env file.
- Nginx configuration files can be added/modified in the ./nginx/conf.d/ directory.
