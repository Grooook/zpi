docker-compose down
docker volume rm -f zpi-2022_postgres_data
docker-compose up --build -d

docker-compose exec web rm -R api/migrations
docker-compose exec web python manage.py flush --no-input
docker-compose exec web python manage.py makemigrations api
docker-compose exec web python manage.py migrate api
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py compilemessages
sleep 3
docker-compose exec web python manage.py loaddata department_fixture
docker-compose exec web python manage.py loaddata users_fixture
docker-compose exec web rm -R media/documents
#docker-compose exec web python manage.py shell -c "from api.models import User; User.objects.create_superuser('admin@example.com', 'Admin Admin', 'admin name', 'admin surname', 'admin')"
#docker-compose exec web python manage.py shell -c "from api.models import User; User.objects.create_user('248795@example.com', 'pwr342784', 'Hleb', 'Liaonik', 'pass')"
