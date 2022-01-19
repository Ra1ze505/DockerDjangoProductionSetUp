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
### On windows:
```
standard_init_linux.go:228: exec user process caused: no such file or directory
```
#### you need change separotors CRLF -> LF

### On Linux:
```
ERROR: for web  Cannot start service web: OCI runtime create failed: container_linux.go:380: starting container process caused: exec: "/home/app/web/entrypoint.prod.sh": permission denied: unknown
```
#### you need:
```
chmod +x entrypoint.prod.sh 
```

