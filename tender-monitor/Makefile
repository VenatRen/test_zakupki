up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

worker:
	docker compose logs -f worker

beat:
	docker compose logs -f beat

test:
	docker compose run --rm api pytest

shell:
	docker compose exec api bash

db:
	docker compose exec postgres psql -U tender -d tenders

restart:
	docker compose restart
