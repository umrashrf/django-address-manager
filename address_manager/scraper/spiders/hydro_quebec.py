import json
import logging
import base64
import boto3

from scrapy_splash import SplashRequest, SplashFormRequest
from loginform import fill_login_form
from dynamic_scraper.spiders.django_spider import DjangoSpider

from address_manager.scraper import settings
from address_manager.models import AddressWebsite, Address, AddressItem


class HydroQuebec(DjangoSpider):

    name = 'hydro_quebec'

    splash_args = {
        'html': 1,
        'png': 1,
        'width': 600,
        'render_all': 1,
        'wait': 1,
    }

    def __init__(self, *args, **kwargs):
        self._set_ref_object(AddressWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.rpt_mp = self.scraper.get_main_page_rpt()
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Address
        self.scraped_obj_item_class = AddressItem
        self.s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL)
        self.s3.create_bucket(Bucket=self.name)
        super().__init__(self, *args, **kwargs)

    def parse(self, response):
        # because following request is a new Splash request
        response.meta.pop('splash')
        response.meta.pop('_splash_processed')

        yield SplashRequest(response.url, self.login,
                            endpoint='render.json',
                            args=self.splash_args,
                            dont_filter=True,
                            meta=response.meta)

    def login(self, response):
        self.s3.Bucket(self.name).put_object(Key='login.png',
                                             Body=base64.b64decode(response.data['png']))
        # logging.debug('Screenshot: %s', response.data['png'])

        try:
            headers = json.loads(self.rpt_mp.headers)
        except json.decoder.JSONDecodeError as err:
            headers = {}
        formdata, url, method = fill_login_form(response.url,
                                                response.text,
                                                response.meta['username'],
                                                response.meta['password'])

        # because following request is a new Splash request
        response.meta.pop('splash')
        response.meta.pop('_splash_processed')

        return SplashFormRequest.from_response(response,
                                                endpoint='render.json',
                                                args=self.splash_args,
                                                headers=headers,
                                                dont_filter=True,
                                                formname='fm',
                                                formdata=formdata,
                                                meta=response.meta,
                                                callback=self.after_login)

    def after_login(self, response):
        self.s3.Bucket(self.name).put(Key='after_login.png',
                                      Body=base64.b64decode(response.data['png']))
        #logging.debug('Screenshot: %s', response.data['png'])
        return super().parse(response)
