import pylast
import vk
import time
import argparse
import sys

def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-vl', '--vk-login', default = None)
	parser.add_argument('-vp', '--vk-password', default = None)
	parser.add_argument('-va', '--vk-album', default = None)

	return parser

if __name__ == '__main__':
	parser = create_parser()
	namespace = parser.parse_args(sys.argv[1:])

	if not namespace.vk_login and not namespace.vk_password and not namespace.vk_album:
		print('You should use all flags!')
		sys.exit()

	session = vk.AuthSession(app_id='5513659', user_login = namespace.vk_login, user_password = namespace.vk_password, scope = 'photos,offline')
	vk_api = vk.API(session)

	me = vk_api.users.get()
	current_id = me[0]['uid']

	while True:
		photos = vk_api.photos.get(owner_id = current_id, album_id = 'saved', count = 1000)
		for photo in photos:
			vk_api.photos.move(owner_id = current_id, target_album_id = namespace.vk_album, photo_id = photo['pid'])
			time.sleep(1)

		time.sleep(1)
