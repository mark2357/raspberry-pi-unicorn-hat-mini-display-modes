'''contains class that displays textdisplays text'''

import time

from helpers.fetch_html_data_from_url import fetch_html_and_extract_data_from_url
from modes.scrolling_text_base_mode import ScrollingTextBaseMode




class Covid19NewCasesTextMode(ScrollingTextBaseMode):
    '''displays the current covid 19 cases for victoria today'''

    def __init__(self, unicornhatmini, config):
        self.last_data_update = time.time()
        self.current_string = 'error could not retrieve data'
        self.update_data()
        super().__init__(unicornhatmini, config)


    def update_current_text(self):
        self.check_update_data()
        self.set_current_text(self.current_string)


    def check_update_data(self):
        '''checks to determine if the current data is out of date'''
        # how often the mode should update the data
        update_interval = float(self.config['COVID_VIC_NEW_CASES_MODE']['UPDATE_INTERVAL'])

        if self.last_data_update + update_interval < time.time():
            self.update_data()
            self.last_data_update = time.time()


    def update_data(self):
        '''gets data from url and updates current string'''
        output = self.extract_string_from_webpage()
        if output is not None:
            self.current_string = output


    def extract_string_from_webpage(self):
        '''extracts data from webpage'''

        data = fetch_html_and_extract_data_from_url('https://covidlive.com.au/vic')

        table = data.find("table", class_="DAILY-CASES")
        if table is None:
            print('error could not find table')
            return None

        table_rows = table.findAll('tr')

        if table_rows is None:
            print('error could not find table_rows in table')
            return None

        output_data = []

        for table_row in table_rows:
            # skips the header
            if table_row.get('class') == ['TH']:
                continue

            cases = table_row.find('td', class_='NET').find('span').decode_contents()
            date = table_row.find('td', class_='DATE').decode_contents()
            day = dict()
            day['date'] = date
            day['cases'] = cases
            output_data.append(day)

        todays_data = output_data[len(output_data) - 1]
        yesterdays_data = output_data[len(output_data) - 2]
        output_string = ''
        if todays_data['cases'].strip() == '':
            output_string = f"todays cases haven't been released yet but yesterday had {yesterdays_data['cases']} cases"
        else:
            output_string = f"today had {todays_data['cases']} new cases compared to yesterdays {yesterdays_data['cases']}"
        return output_string
