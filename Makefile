stop:
	docker-compose down

start:
	docker-compose build && docker-compose up -d

restart: stop start

test: start
	echo "Waiting 10 seconds to let db and cache load and connect" && sleep 10s && python3 unit_test.py

