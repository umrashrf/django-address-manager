import json
import logging

from scrapy_splash import SplashRequest, SplashFormRequest
from loginform import fill_login_form
from dynamic_scraper.spiders.django_spider import DjangoSpider

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
        super().__init__(self, *args, **kwargs)

    def parse(self, response):
        # because following request is a new Splash request
        response.meta.pop('splash')
        response.meta.pop('_splash_processed')

        yield SplashRequest(response.url, self.login, endpoint='render.json',
                            args=self.splash_args, dont_filter=True, meta=response.meta)


    def login(self, response):
        logging.debug('<img src="data:image/png;base64,%s" />',
                      response.data['png'])

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
        logging.debug('<p><img src="data:image/png;base64,%s" /></p>',
                      response.data['png'])
        return super().parse(response)
