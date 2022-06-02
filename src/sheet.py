from __future__ import print_function
from urllib import response

import pytz
import pickle
import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleSheetClient(object):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self):
        self.creds = None
        self._init_spreadsheet_service()

    def _init_spreadsheet_service(self):
        if not os.path.exists(os.getcwd() + '/credentials.json'):
            raise Exception("credentials.json not found")

        self.creds = service_account.Credentials.from_service_account_file(os.getcwd() + '/credentials.json', 
            scopes=GoogleSheetClient.SCOPES)
        
        self.service = build('sheets', 'v4', credentials=self.creds)

class GoogleSheetEditor():
    def __init__(self, sheet_id, sheet_name, title_rows=3):
        self.client = GoogleSheetClient()
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        # reserved rows for extra information like 
        # title and description of the spreadsheet
        self.title_rows = title_rows
        
    def _column_to_letter_identifier(self, column_id):
        t, l = '', ''
        while (column_id > 0):
            t = (column_id - 1) % 26
            l = chr(t + 65) + l
            column_id = int((column_id - t - 1) / 26)
        return l

    def get_sheet_range(self):
        return "{}!{}{}:Z".format(
            self.sheet_name, 'A', self.title_rows+1)
    
    def get_custom_range(self, start, end):
        return "{}!{}:{}".format(
            self.sheet_name, start, end)

    def read_custom(self, start, end, indexField=None):
        return self.client.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id, range=self.get_custom_range(start, end)).execute()['values']

    def read_spreadsheet(self, indexField=None):
        return self.from_sheet_data(self.client.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id, range=self.get_sheet_range()).execute()['values'], indexField)
    
    def load_data_from_sheet(self):
        return self.from_sheet_data(self.sheet.get('values', []))

    def save_data_to_sheet(self, rows):
        body = { 'values': self.to_sheet_data(rows) }
        responses = []
        responses.append(self.clear_previous_data())
        responses.append(self._update_timestamp())
        responses.append(self.client.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id, range=self.get_sheet_range(),
            valueInputOption='USER_ENTERED', body=body).execute())
        return responses

    def append_data_to_sheet(self, rows):
        body = { 'values': self.to_sheet_data(rows, skip_labels=True) }
        responses = []
        responses.append(self._update_timestamp())
        responses.append(self.client.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id, range="{}!A{}".format(self.sheet_name, self.title_rows+2),
            valueInputOption='USER_ENTERED', body=body, insertDataOption='INSERT_ROWS').execute())
        return responses

    def clear_previous_data(self):
        return self.client.service.spreadsheets().values().clear(
            spreadsheetId=self.sheet_id, range=self.get_sheet_range()).execute()
        
    def _update_timestamp(self):
        now = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime("%H:%M:%S %B %d, %Y")
        body = { 'values': [['Updated On', '{}'.format(now)]] }
        return self.client.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id, range="{}!{}".format(self.sheet_name, 'A3'),
            valueInputOption='USER_ENTERED', body=body).execute()

    def from_sheet_data(self, data, indexField=None):
        """ loads spredsheet data into list of dicts 
        """
        if indexField == None:
            converted_data = []
        else:
            converted_data = {}
        columns = data[0]
        for row in data[1:]:
            row_dict = {}
            while len(row) > len(columns):
                columns.append('')  
            while len(columns) > len(row):
                row.append('')   
            for idx, row_item in enumerate(row):
                row_dict[columns[idx]] = row_item
            if indexField == None:
                converted_data.append(row_dict)
            else:
                converted_data[row_dict[indexField]] = row_dict
        return converted_data

    def to_sheet_data(self, rows, skip_labels=False):
        """ converts list of dicts into sheet compatible format
        """
        data = []
        column_labels = []
        for row in rows:
            for k, v in row.items():
                if k not in column_labels:
                    column_labels.append(k)
            current_row = ['']*(max(len(column_labels), len(row.keys())))
            for k, v in row.items():
                idx = column_labels.index(k)
                if isinstance(v, datetime.date):
                    v = v.strftime("%m/%d/%Y")
                current_row[idx] = v
            data.append(current_row)
        if skip_labels:
            return data
        return [column_labels]+data


def format_sheet():

    client = GoogleSheetClient()

    request_body = {

        'requests':[
            # All Instances
            {
            'repeatCell': {

                'range': {
                    'sheetId' : 0, 
                    'startRowIndex': 3,
                    'endRowIndex' : 4,
                    'startColumnIndex':0,
                    'endColumnIndex':10
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 117,
                            'green':59,
                            'blue':25
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        },{
            'repeatCell': {

                'range': {
                    'sheetId' : 0, 
                    'startRowIndex': 2,
                    'endRowIndex' : 3,
                    'startColumnIndex':0,
                    'endColumnIndex':2
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 19,
                            'green':75,
                            'blue':219
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            },
        },
            ## All cluster Instances
            {
            'repeatCell': {

                'range': {
                    'sheetId' : 1587125586, 
                    'startRowIndex': 3,
                    'endRowIndex' : 4,
                    'startColumnIndex':0,
                    'endColumnIndex':10
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 117,
                            'green':59,
                            'blue':25
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
            },
            {
            'repeatCell': {

                'range': {
                    'sheetId' : 1587125586, 
                    'startRowIndex': 2,
                    'endRowIndex' : 3,
                    'startColumnIndex':0,
                    'endColumnIndex':2
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 19,
                            'green':75,
                            'blue':219
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            },
            },

            #Cost Summary

             {'repeatCell': {

                'range': {
                    'sheetId' : 1239517681, 
                    'startRowIndex': 2,
                    'endRowIndex' : 3,
                    'startColumnIndex':0,
                    'endColumnIndex':2
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 19,
                            'green':75,
                            'blue':219
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
    },{
            'repeatCell': {

                'range': {
                    'sheetId' : 1239517681, 
                    'startRowIndex': 3,
                    'endRowIndex' : 4,
                    'startColumnIndex':0,
                    'endColumnIndex':2
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 117,
                            'green':59,
                            'blue':25
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }},{
             'repeatCell': {

                'range': {
                    'sheetId' : 1239517681, 
                    'startRowIndex': 4,
                    'startColumnIndex':1,
                    'endColumnIndex':2
                },
                'cell':{
                    'userEnteredFormat':{
                        'numberFormat':{
                            'type':'CURRENCY',
                            'pattern':'$#,##.00'
                        },
                        'textFormat':{
                            'fontSize':11,
                            'bold':True
                        }
                    }
                },
            'fields': 'userEnteredFormat(numberFormat,textFormat)'
            }},
            
            ## Instances cost
            {
            'repeatCell': {

                'range': {
                    'sheetId' : 755432813, 
                    'startRowIndex': 2,
                    'endRowIndex' : 3,
                    'startColumnIndex':0,
                    'endColumnIndex':2
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 19,
                            'green':75,
                            'blue':219
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }

            },{

                'repeatCell': {

                'range': {
                    'sheetId' : 755432813, 
                    'startRowIndex': 3,
                    'endRowIndex' : 4,
                    'startColumnIndex':0,
                    'endColumnIndex':11
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 117,
                            'green':59,
                            'blue':25
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }},{
                'repeatCell': {

                'range': {
                    'sheetId' : 755432813, 
                    'startRowIndex': 4,
                    'startColumnIndex':10,
                    'endColumnIndex': 11
                },
                'cell':{
                    'userEnteredFormat':{
                        'numberFormat':{
                            'type':'CURRENCY',
                            'pattern':'$#,##.00'
                        },
                        'textFormat':{
                            'fontSize':11,
                            'bold':True
                        }
                    }
                },
            'fields': 'userEnteredFormat(numberFormat,textFormat)'
            }

            },
            

            ##Old Clusters
            {
                'repeatCell': {

                'range': {
                    'sheetId' : 42437603, 
                    'startRowIndex': 2,
                    'endRowIndex' : 3,
                    'startColumnIndex':0,
                    'endColumnIndex':2
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 19,
                            'green':75,
                            'blue':219
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },{
                 'repeatCell': {

                'range': {
                    'sheetId' : 42437603, 
                    'startRowIndex': 3,
                    'endRowIndex' : 4,
                    'startColumnIndex':0,
                    'endColumnIndex':6
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 117,
                            'green':59,
                            'blue':25
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },


            ## All Clusters

            {
                'repeatCell': {

                'range': {
                    'sheetId' : 846402724, 
                    'startRowIndex': 2,
                    'endRowIndex' : 3,
                    'startColumnIndex':0,
                    'endColumnIndex':2
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 19,
                            'green':75,
                            'blue':219
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },{
                 'repeatCell': {

                'range': {
                    'sheetId' : 846402724, 
                    'startRowIndex': 3,
                    'endRowIndex' : 4,
                    'startColumnIndex':0,
                    'endColumnIndex':6
                },
                'cell':{
                    'userEnteredFormat':{
                        'backgroundColor':{
                            'red': 117,
                            'green':59,
                            'blue':25
                        },
                        'textFormat':{
                            'fontSize':12,
                            'bold':True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            }
            
            ]
    }

    response = client.service.spreadsheets().batchUpdate(
        spreadsheetId = os.getenv("SHEET_ID"),
        body = request_body
    ).execute()


   