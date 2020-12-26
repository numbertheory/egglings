
docker:
	docker build -t egglings:main -f Dockerfile .

egglings:
	@docker run -t -v ${PWD}/exercises:/app/exercises egglings:main
