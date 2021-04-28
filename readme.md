##### Setup instructions (virtualenv):
```
1. make python3 virtualenv and activate it
2. pull repo
3. cd directory
4. pip install -r requirements.txt
5. ./manage.py migrate
6. ./manage.py createsuperuser
7. ./manage.py runserver
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
/directory/teachers/<teacher_id>
```
