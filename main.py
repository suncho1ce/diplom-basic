import json
import os
import requests
import datetime


class VK:

    def __init__(self, vk_token, user_id, version='5.131'):
        self.token = vk_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def export_avatars(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': 5
        }
        response = requests.get(url, params={**self.params, **params}).json()
        avatars_count = response['response']['count']
        print(f'Количество фотографий профиля id{user_id}: {avatars_count}')
        count = 0
        if avatars_count > 0:
            if avatars_count < 6:
                print(f'Но мы скачаем только {avatars_count}')
            if avatars_count > 5:
                print(f'Но мы скачаем только 5')
                avatars_count = 5
            YaUploader(ya_token).create_folder()
            for item in response['response']['items']:
                date_time = (datetime.datetime.fromtimestamp(item['date'])).strftime('%d%m%Y_%H%M%S')
                vk_file_url = item['sizes'][-1]['url']
                likes = item['likes']['count']
                file_name = str(likes) + '.jpg'
                for name in info_file:
                    if file_name in name['file_name']:
                        file_name = str(likes) + '_' + date_time + '.jpg'
                size_type = item['sizes'][-1]['type']
                info_file.append({'file_name': file_name, 'size': size_type})
                path = user_id + '/' + file_name
                YaUploader(ya_token).upload_file_url(path, vk_file_url)
                count += 1
                print(f'Обработано изображений {count} из {avatars_count}')

            if (os.path.isfile('info_file.json')):
                os.remove('info_file.json')

            with open('info_file.json', 'w', encoding='utf-8') as info_file_offline:
                json.dump(info_file, info_file_offline)

            path_json_file = user_id + '/' + 'info_file.json'
            YaUploader(ya_token).upload(path_json_file, 'info_file.json')
            print(f'Файлы успешно загружены: https://disk.yandex.ru/client/disk/{user_id}')
            return
        else:
            print('У этого юзера аватарок нет!')


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self):
        path_create_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        requests.put(f'{path_create_url}?path={user_id}', headers=headers)

    def upload_file_url(self, path: str, vk_file_url: str):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': path, 'url': vk_file_url}
        requests.post(upload_url, headers=headers, params=params)

    def upload(self, file_path: str, info_filename: str):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        href = response.json().get('href', '')
        requests.put(href, data=open(info_filename, 'rb')) #


info_file = []
user_id = ''
ya_token = ''
vk_token = 'vk1.a.xFJmi14BMR1PDxNY8zEqUGTtFouWbQMt_27FzSHDvRo-5XLVwu3hph4NjjrV9AjZNHtpZ7EG-WOM87su6DwWOn576HRcYHTf0QAeH9Jee45IQ0Cw1z1hIG-_eRh2IOopo3Ef9i2vnTT1e5BxN5YknIg9zdaOr1pPPAxcmF2cMVxyt5gr29j2m6LtrTlUy62E'
vk = VK(vk_token, user_id)

if __name__ == '__main__':
    vk.export_avatars()