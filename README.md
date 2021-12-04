
# Mazaryn Social Network
![GitHub top language](https://img.shields.io/github/languages/top/mazarynxyz/mazaryn)
![GitHub last commit](https://img.shields.io/github/last-commit/mazarynxyz/mazaryn)
![GitHub repo size](https://img.shields.io/github/repo-size/mazarynxyz/mazaryn)
![GitHub](https://img.shields.io/github/license/mazarynxyz/mazaryn)
![Twitter Follow](https://img.shields.io/twitter/follow/mazaryn)

## Description

> Distributed Social Network that allows users interact with each other as well as offering a social market place platform.

## Prerequsites

> The following depenencies need to be installed for smooth running
>
> 1. django
> 2. pillow
> 3. django restframework
> 4. django-cors-headers
> 5. channels
> 6. channels-redis
> 7. djoser
> 8. django-friendship
> 9. drf_yasg

> Open terminal/command prompt and run:
>
> - `python manage.py migrate`
> - `python manage.py createsuperuser`



### Set up postgres guide for linux:

1. Install postgres
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

2. Access postgres console:
`sudo -i -u postgres `
OR 
`sudo -u postgres psql`


3. change password command f
`\password postgres`

4. Add database
`create database mazaryn;`

5. Set following os constants
```
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
DATABASE_HOST
DATABASE_PORT
```


5. Migrate models:
`python manage.py migrate`

### For mac users, please make the following adjustments before installing the dependencies

1. Install `Rust` (use `brew`)
2. Install `libmagic` (use `brew`)
3. Update `pip` to the latest version
