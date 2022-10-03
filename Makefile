up:
	docker-compose up -d --build

down:
	docker-compose down

test:
	docker-compose exec web pytest .

alembic-init:
	docker-compose exec web alembic init -t async migrations

alembic-autogenerate:
	docker-compose exec web alembic revision --autogenerate -m "$(mes)"

alembic-upgrade:
	docker-compose exec web alembic upgrade head

