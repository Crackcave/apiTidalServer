build:
	docker build --tag api-tidal-server .

run:
	docker stop api_tidal_server | true
	docker rm api_tidal_server | true
	docker run -p 5222:5222 -d --network=dde -ti --name api_tidal_server api-tidal-server

logs:
	docker logs -f api_tidal_server