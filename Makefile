up:
	docker-compose up -d --build

down:
	docker-compose down

test:
	docker-compose exec web pytest . -v -rsxX

test-short:
	docker-compose exec web pytest -v -rsxX -l --tb=short --strict -p no:warnings

alembic-init:
	docker-compose exec web alembic init -t async migrations

alembic-autogenerate:
	docker-compose exec web alembic revision --autogenerate -m "$(mes)"

alembic-upgrade:
	docker-compose exec web alembic upgrade head

