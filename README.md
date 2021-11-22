# Seznam Sklik - Test #

## How to execute app
1. Run "docker-compose up" on your local machine
2. Access http://localhost:5000/impressions to fetch impressions
3. Access http://localhost:5000/impressions to fetch clicks

## Database login
In order to login use the following commands:
- docker exec -it seznam-test-db-1 bash
- mysql -u root -p (password: 'seznam123')


## Notes 
- To access admin site go to http://0.0.0.0:8080/ (system: mysql, server: db, user: root, password: 'seznam123')
- To run flask locally: FLASK_APP=app.py FLASK_ENV=development flask run 

## Docker
In case you need to rebuild app container:
- docker-compose down 
- docker-compose build --no-cache