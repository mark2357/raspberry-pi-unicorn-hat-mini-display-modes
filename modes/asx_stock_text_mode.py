'''contains class that displays stock information from the asx website'''

import time
import ast
from helpers.fetch_html_data_from_url import fetch_html_and_extract_data_from_url
from modes.scrolling_text_base_mode import ScrollingTextBaseMode




class ASXStockTextMode(ScrollingTextBaseMode):
    '''displays the current asx stock information for chosen stocks'''

    def __init__(self, unicornhatmini, config):
        self.last_data_update = time.time()
        self.current_data = []
        self.display_string_index = 0
        self.config = config
        self.update_data()
        super().__init__(unicornhatmini, config)


    def update_current_text(self):
        '''overrides method to update text'''
        self.check_update_data()

        current_data = self.current_data[self.display_string_index]
        new_string = current_data['text']

        # color_r, color_g, color_b is defined in ScrollingTextBaseMode
        if current_data['price_up'] is True:
            self.set_rgb(0, 255, 0)
        elif current_data['price_up'] is None:
            self.set_rgb(255, 255, 255)
        else:
            self.set_rgb(255, 0, 0)


        self.display_string_index = self.display_string_index + 1
        if self.display_string_index >= len(self.current_data):
            self.display_string_index = 0

        self.set_current_text(new_string)


    def check_update_data(self):
        '''checks to determine if the current asx data is out of date'''
        # how often the mode should update the data
        update_interval = self.config.getfloat('ASX_STOCK_TEXT_MODE', 'UPDATE_INTERVAL', fallback=300)

        if self.last_data_update + update_interval < time.time():
            self.update_data()
            self.last_data_update = time.time()

    def update_data(self):
        '''gets data from url and updates current string'''

        stock_codes_array_string = self.config.get('ASX_STOCK_TEXT_MODE', 'STOCK_CODES', fallback="['TLS']")
        try:
            stock_codes = ast.literal_eval(stock_codes_array_string)
        except SyntaxError:
            print('ERROR invalid stock codes using default')
            stock_codes = ['TLS']

        current_data = []
        for stock_code in stock_codes:
            stock_info = self.get_stock_info(stock_code)
            if stock_info is not None:
                current_data.append(stock_info)

        self.current_data = current_data


    def get_stock_info(self, stock_code):
        '''extracts data from webpage and returns dictionary'''

        last_price = 0
        price_up = None
        try:
            data = fetch_html_and_extract_data_from_url(f'https://www.asx.com.au/asx/markets/priceLookup.do?by=asxCodes&asxCodes={stock_code}')
            table = data.find("table", class_="datatable")
            if table is None:
                print('ERROR could not find table with stock data within webpage')
                return None

            table_rows = table.findAll('tr')

            if table_rows is None:
                print('ERROR could not find table_rows in table')
                return None

            first_row = True

            for table_row in table_rows:

                # skips the first row as it's the header
                if first_row is True:
                    first_row = False
                    continue

                last_tag = table_row.find('td', class_='last')
                price_change_img = last_tag.find('img')
                if price_change_img is not None:
                    # occurs at start of day price hasn't gone up or down yet
                    price_up = price_change_img['alt'] == 'Up'
                    last_tag.img.unwrap()

                last_price = last_tag.decode_contents().strip()

        except:
            print(f'ERROR in processing data from webpage for asx code {stock_code}')
            return None


        stock_info = dict()

        if self.config.getboolean('ASX_STOCK_TEXT_MODE', 'SHORTEN_TEXT', fallback=False):
            stock_info['text'] = f'{stock_code} is {last_price}'
        else:
            stock_info['text'] = f'The Current Price for {stock_code} is {last_price}'

        stock_info['price_up'] = price_up

        return stock_info
