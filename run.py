import vk
import time
import argparse
import sys
import wget
import subprocess
import requests
import json
import os

# default sleep time
def sleep():
	time.sleep(1)

def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-vl', '--vk-login', default = None)
	parser.add_argument('-vp', '--vk-password', default = None)
	parser.add_argument('-t', '--text', default=None)
	parser.add_argument('-va', '--vk-album', default = None)

	return parser

if __name__ == '__main__':
	parser = create_parser()
	namespace = parser.parse_args(sys.argv[1:])

	if not namespace.vk_login and not namespace.vk_password and not namespace.vk_album and not namespace.text:
		print('You should use all flags!')
		sys.exit()

	session = vk.AuthSession(
		app_id='5513659', 
		user_login = namespace.vk_login, 
		user_password = namespace.vk_password, 
		scope = 'photos,offline')

	vk_api = vk.API(session)

	me = vk_api.users.get()
	current_id = me[0]['uid']

	while True:
		photos = vk_api.photos.get(owner_id = current_id, album_id = 'saved', count = 1000)
		for photo in photos:
			# download picture
			tempfile = wget.download(photo['src_big'])
			# apply watermark
			subprocess.call([
			'convert',
			tempfile,
			'-gravity', 'SouthEast',
			'-font', 'Ubuntu-Mono-Bold',
			'-pointsize', '30',
			'-fill', 'white',
			'-undercolor', '#00000080',
			'-annotate', '+5+5', namespace.text,
			tempfile])

			# upload photo to vk
			upload_server = vk_api.photos.getUploadServer(album_id = namespace.vk_album)
			sleep()

			response = requests.post(upload_server['upload_url'], files={'file1': (tempfile, open(tempfile, 'rb'))})
			result = json.loads(response.text)

			vk_api.photos.save(
				album_id = namespace.vk_album,
				server = result['server'],
				photos_list = result['photos_list'],
				hash = result['hash'],
				)

			# remove from vk
			photos = vk_api.photos.delete(owner_id = current_id, photo_id = photo['pid'])
			# remove tempfile
			os.remove(tempfile)
			sleep()

		sleep()