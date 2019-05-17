import sys
import pickle
import os.path
from investment import Investment
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_SPREADSHEET_ID = '1TE4mjYDjDBeLbHbSlOEeU5k-H9lP2A9DEae7sktgGbo'
SAMPLE_RANGE_NAME = 'A2:G12'

class InvestmentPortfolio():
    def __init__(self):
        self.google_spreadsheet_id  = '1TE4mjYDjDBeLbHbSlOEeU5k-H9lP2A9DEae7sktgGbo'
        self.google_sheet_id        = 0
        self.service                = ''
        self.portfolio              = dict() #need to read csv file and then add to it
        self.investment             = Investment()
    
    def __validate_google_credentials(self):
        """validates user credentials 
        user must give authorization of user data
        """
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow    = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds   = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def company_share_owned(self, ticker):
        """returns true if company share is owned"""
        self.__validate_google_credentials()
        sheet   = self.service.spreadsheets()
        result  = sheet.values().get(spreadsheetId=self.google_spreadsheet_id,
                                    range=self.__get_portfolio_range()[1]).execute()
        values  = result.get('values', [])
        for row in values:
            if ticker == row[1]:
                return True
        return False

    def __get_portfolio_range(self):
        """"returns a tuple of (next_new_row, range)"""
        print('start')
        self.__validate_google_credentials()
        sheet   = self.service.spreadsheets()
        r = 'A'
        r_num = 2
        result  = sheet.values().get(spreadsheetId=self.google_spreadsheet_id,
                                    range=r+str(r_num)).execute()
        while(len(result.get('values', [])) != 0):
            r_num += 1
            result = sheet.values().get(spreadsheetId=self.google_spreadsheet_id,
                                    range=r+str(r_num)).execute()
        print('done')
        return ( r + str(r_num) + ':G' + str(r_num), r + '2:G' + str(r_num-1))
         
    def add_option_purchase(self, ticker, category, num_shares, buy_price):
        """updates sheet with new option purchase info"""
        ranges          = self.__get_portfolio_range()
        company         = self.investment.get_company_name(ticker)
        ownership       = '[OWN]' #change font color
        category        = 'CALL' #change font color
        current_price   = self.investment.get_current_price(ticker)
        body_request    = { "range": ranges[0],
                            "majorDimension": 'ROWS',
                            "values": [
                                [company, ticker, ownership, category, num_shares, buy_price, current_price]
                            ]
                            }
        #update excel sheet
        self.__validate_google_credentials()
        sheet   = self.service.spreadsheets()
        result  = sheet.values().update(spreadsheetId=self.google_spreadsheet_id,
                                    range=ranges[0], valueInputOption='USER_ENTERED', body=body_request).execute()
        print('values:',  [])
        
    def add_share_purchase(self, ticker, category, num_shares, buy_price):
        company         = self.investment.get_company_name(ticker)
        ownership       = '[OWN]' #change font color
        category        = 'STOCK'
        current_price   = self.investment.get_current_price(ticker)
        pass

    def expired_share(self, ticker):
        pass

    def sold_share(self, ticker):
        pass

    def loss_color(self):
        pass

    def gain_color(self):
        pass

    def update_price(self, ticker):
        pass

    def print_portfolio(self):
        """printing out values pulled from sheet"""
        self.__validate_google_credentials()
        sheet   = self.service.spreadsheets()
        result  = sheet.values().get(spreadsheetId=self.google_spreadsheet_id,
                                    range=self.__get_portfolio_range()[1]).execute()
        values  = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('pulled data:')
            print('----------------')
            print('ALL VALUES\n', '-----------------\n', values)
            print('ONLY PRICES\n', '----------------')
            print('{:25}    {}'.format('name', 'price'))
            
            for row in values:
                if len(row) < 7 or row[2] != '[OWN]':
                    continue
                else:
                    print('{:25}    {}'.format(row[0], row[6]))

    def print_update_queue():
        pass

    def update_portfolio():
        pass


if __name__ == "__main__":
    test = InvestmentPortfolio()
    ticker = sys.argv[1]
    #test.add_option_purchase(ticker, 'test test', 10, 2.32)
    if test.company_share_owned(ticker):
        test.print_portfolio()
    else:
        print('You do not own shares of this company yet!')
    
