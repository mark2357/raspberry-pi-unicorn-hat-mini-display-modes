'''contains class that displays textdisplays text'''

import time

from helpers.fetch_html_data_from_url import fetch_html_and_extract_data_from_url
from modes.scrolling_text_base_mode import ScrollingTextBaseMode




class Covid19NewCasesTextMode(ScrollingTextBaseMode):
    '''displays the current covid 19 cases for victoria today'''

    def __init__(self, unicornhatmini, config, custom_options=None):
        self.last_data_update = time.time()
        self.current_string = 'error could not retrieve data'
        self.update_data()
        super().__init__(unicornhatmini, config, custom_options)


    def update_current_text(self):
        '''overrides method to update text'''
        self.check_update_data()
        self.set_current_text(self.current_string)


    def check_update_data(self):
        '''checks to determine if the current data is out of date'''
        # how often the mode should update the data
        update_interval = self.config.getfloat('COVID_VIC_NEW_CASES_MODE', 'UPDATE_INTERVAL', fallback=300)

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


        output_data = []
        try:
            data = fetch_html_and_extract_data_from_url('https://covidlive.com.au/vic')

            table = data.find("table", class_="DAILY-CASES")
            if table is None:
                print('error could not find table')
                return None

            table_rows = table.findAll('tr')

            if table_rows is None:
                print('error could not find table_rows in table')
                return None


            for table_row in table_rows:
                # skips the header
                if table_row.get('class') == ['TH']:
                    continue

                date = table_row.find('td', class_='DATE').decode_contents()

                cases_cell = table_row.find('td', class_='NET')
                cases_cell_span = cases_cell.find('span')
                # will occur when cases haven't been released yet
                if cases_cell_span is None and cases_cell.decode_contents() == '-':
                    cases = None
                # will occur when cases have been released
                else:
                    cases = cases_cell_span.decode_contents()

                day = dict()
                day['date'] = date
                day['cases'] = cases
                output_data.append(day)

        except:
            print('error in processing data from webpage for covid 19 new cases text mode')
        if len(output_data) > 1:
            todays_data = output_data[len(output_data) - 1]
            yesterdays_data = output_data[len(output_data) - 2]
            output_string = ''
            if todays_data['cases'] is None:
                output_string = f"todays cases haven't been released yet but yesterday had {yesterdays_data['cases']} cases"
            else:
                output_string = f"today had {todays_data['cases']} new cases compared to yesterdays {yesterdays_data['cases']}"
            return output_string
        else:
            return 'Error in retreving data'
