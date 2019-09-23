import json

from scrapy_splash import SplashRequest, SplashFormRequest
from loginform import fill_login_form
from dynamic_scraper.spiders.django_spider import DjangoSpider

from address_manager.models import AddressWebsite, Address, AddressItem


class HydroQuebec(DjangoSpider):
    
    name = 'hydro_quebec'

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
        try:
            headers = json.loads(self.rpt_mp.headers)
        except json.decoder.JSONDecodeError as err:
            headers = {}    
        formdata, url, method = fill_login_form(response.url,
                                                response.text, 
                                                response.meta['username'], 
                                                response.meta['password'])
        return SplashFormRequest.from_response(response,
                                                headers=headers,
                                                dont_filter=True,
                                                formname='fm', 
                                                formdata=formdata,
                                                meta=response.meta, 
                                                callback=super().parse)
