##### Setup instructions (virtualenv):
```
1. pull repo
2. cd directory
3. pip install -r requirements.txt
4. ./manage.py createsuperuser
5. ./manage.py runserver
```

##### Setup instructions (docker):

```
1. pull repo
2. cd directory
3. docker-compose up -d
4. find docker container id (docker ps)
5. docker exec -it [container_id] ./manage.py createsuperuser
```
##### Available endpoints:
```
/directory/uploader/
/directory/teachers/
```
