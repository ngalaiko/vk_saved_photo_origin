rebuild:
	docker build -t vk_saved_photo_origin .
	docker rm -f docker run -d --name site --network=host --restart=always site
	docker run -d --name vk_saved_photo_origin --network=host --restart=always vk_saved_photo_origin
	docker rmi $(docker images | grep '<none>' | awk '{ print $3; }')
