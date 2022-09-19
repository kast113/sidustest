up:
	docker-compose up -d --build

down:
	docker-compose down

test:
	docker-compose exec web pytest .
