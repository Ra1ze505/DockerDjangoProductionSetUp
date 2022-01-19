# DockerSetUp
## Fast install
#### Create clone:
```
git clone https://github.com/Ra1ze505/DockerSetUp.git
```

#### Create at the root of the project file `.env`, example:

```
DEBUG=1
SECRET_KEY=change_me
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_prod
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

#### Create at the root of the project file `.env.db`, example:

``` 
POSTGRES_USER=hello_django
POSTGRES_PASSWORD=hello_django
POSTGRES_DB=hello_django_prod
```

#### Up docker-compose:

```
docker-compose up
```

#### Go to http://localhost:8000/backend/swagger
#### WebSockets [ws:/localhost:8001/ws/chat/](ws:/localhost/ws/chat/)
# Exec container:

```
docker-compose exec --user django <container-name> sh
```
#### Activate venv in container exec:

```
source /src/venv/bin/activate
```

# Production start:

#### Create at the root of the project file `.env.prod`, example:

```
DEBUG=0
SECRET_KEY=change_me
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 your.domain.com [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django_prod
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

#### Create at the root of the project file `.env.prod.db`, example:

``` 
POSTGRES_USER=hello_django
POSTGRES_PASSWORD=hello_django
POSTGRES_DB=hello_django_prod
```

###Up containers:
```
sudo docker-compose -f docker-compose.prod.yml up --build -d
```

#### Go to https://localhost/backend/swagger
#### WebSockets [wss:/localhost/ws/chat/](wss:/localhost/ws/chat/)
#### You can see traefik dashboard on https://dashboard-traefik.localhost/

#### For example login: _testuser_ password: _password_

### You can change login in password by using util htpasswd:
```
# username: testuser
# password: password

$ echo $(htpasswd -nb testuser password) | sed -e s/\\$/\\$\\$/g
testuser:$$apr1$$jIKW.bdS$$eKXe4Lxjgy/rH65wP1iQe1
```

#### In docker-compose.prod.yml change this:
```
traefik:
    ...
    labels:
        ...
      - "traefik.http.middlewares.auth.basicauth.users=testuser:$$apr1$$jIKW.bdS$$eKXe4Lxjgy/rH65wP1iQe1"
```

# You may get errors:
### On Windows:
```
standard_init_linux.go:228: exec user process caused: no such file or directory
```
#### or:
```
------
 > [build 8/8] RUN chmod +x ./find_deps.sh     && ./find_deps.sh ./venv/ > deps.txt:
#20 0.446 /bin/sh: ./find_deps.sh: not found
------
executor failed running [/bin/sh -c chmod +x ./find_deps.sh     && ./find_deps.sh ./venv/ > deps.txt]: exit code: 127
ERROR: Service 'web' failed to build : Build failed

```
#### You need change separators CRLF -> LF in files: `entrypoint.sh` and `find_deps.sh`

### On Linux or macOS:
```
ERROR: for web  Cannot start service web: OCI runtime create failed: container_linux.go:380: starting container process caused: exec: "/home/app/web/entrypoint.prod.sh": permission denied: unknown
```
#### you need:
```
chmod +x entrypoint.prod.sh 
```

