import json
from copy import deepcopy
from urllib.parse import urlencode

import scrapy
from scrapy.http import HtmlResponse
from instagram.instagram.items import InstagramItem


class InstaSpider(scrapy.Spider):
    name = "insta"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://instagram.com"]
    inst_login_link = 'https://www.instagram.com/api/v1/web/accounts/login/ajax/'
    inst_login = 'username_login'
    user_for_parse = {'name':'nickname_user_for_parse', 'id':'1234567890'}

    def parse(self, response):
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.authorize,
            formdata={'username': self.inst_login,
                      'enc_password': 'hash_password_from_Fetch/XHR_Network'},
            headers={'X-Csrftoken': 'token_from_Headers_from_Fetch/XHR_Network'}
        )

    def authorize(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            yield response.follow(
                f"/{self.user_for_parse.get('name')}",
                callback=self.user_data_parse,
                cb_kwargs={'username': self.user_for_parse.get('name')}
            )

    def user_data_parse(self, response:HtmlResponse, username):
        user_id = self.user_for_parse.get('id')
        params = {'count': '12'}
        url_posts = f"https://www.instagram.com/api/v1/feed/user/{user_id}/?{urlencode(params)}"

        yield response.follow(
            url_posts,
            callback=self.user_for_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'params': deepcopy(params)},
            headers={'User-Agent': 'Instagram: 244.0.0.17.110'}
        )

    def user_posts_parse(self, response:HtmlResponse, username, user_id, params):
        j_data = response.json()
        next_page = j_data.get('more_available')
        if next_page:
            next_max_id = j_data.get('next_max_id')
            params['max_id'] = next_max_id
            url_posts = f"https://www.instagram.com/api/v1/feed/user/{user_id}/?{urlencode(params)}"

            yield response.follow(
                url_posts,
                callback=self.user_for_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'params': deepcopy(params)},
                headers={'User-Agent': 'Instagram: 244.0.0.17.110'}
            )
        posts = j_data.get('items')
        for post in posts:
            item = InstagramItem(
                text = post.get('caption').get('text'),
                photo = post.get('image_versions2').get('candidates')[0].get('url'),
                # и другие ключи
                post_data = post,
                username = username,
                user_id = user_id
            )

            yield item

    def save_to_json(self, text):
        with open('page.json', 'w') as f:
            json.dump(text, f)

