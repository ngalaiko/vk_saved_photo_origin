rebuild:
	docker rmi $(docker images | grep '<none>' | awk '{ print $3; }'); exit 0;
	docker build -t vk_saved_photo_origin .
	docker run -d --name vk_saved_photo_origin --network=host --restart=always vk_saved_photo_origin