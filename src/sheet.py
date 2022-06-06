from __future__ import print_function

import datetime
import os

import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build


# Class to handle dealing with the Google Sheets API
class GoogleSheetClient(object):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self):
        self.creds = None
        self._init_spreadsheet_service()

    def _init_spreadsheet_service(self):
        if not os.path.exists(os.getcwd() + '/credentials.json'):
            raise Exception("credentials.json not found")

        self.creds = service_account.Credentials.from_service_account_file(
            os.getcwd() + '/credentials.json',
            scopes=GoogleSheetClient.SCOPES
        )

        self.service = build('sheets', 'v4', credentials=self.creds)


# Class to deal with updating, editing, and deleting data within a single sheet
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
            self.sheet_name, 'A', self.title_rows + 1)

    def get_custom_range(self, start, end):
        return "{}!{}:{}".format(
            self.sheet_name, start, end)

    def read_custom(self, start, end, indexField=None):
        return self.client.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=self.get_custom_range(start, end)
        ).execute()['values']

    def read_spreadsheet(self, indexField=None):
        return self.from_sheet_data(self.client.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id,
            range=self.get_sheet_range()
        ).execute()['values'], indexField)

    def load_data_from_sheet(self):
        return self.from_sheet_data(self.sheet.get('values', []))

    def save_data_to_sheet(self, rows):
        body = {'values': self.to_sheet_data(rows)}
        responses = []
        responses.append(self.clear_previous_data())
        responses.append(self._update_timestamp())
        responses.append(
            self.client.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=self.get_sheet_range(),
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
        )
        return responses

    def append_data_to_sheet(self, rows):
        body = {'values': self.to_sheet_data(rows, skip_labels=True)}
        responses = []
        responses.append(self._update_timestamp())
        responses.append(
            self.client.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range="{}!A{}".format(self.sheet_name, self.title_rows + 2),
                valueInputOption='USER_ENTERED',
                body=body,
                insertDataOption='INSERT_ROWS'
            ).execute()
        )
        return responses

    def clear_previous_data(self):
        return self.client.service.spreadsheets().values().clear(
            spreadsheetId=self.sheet_id,
            range=self.get_sheet_range()
        ).execute()

    def _update_timestamp(self):
        now = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime("%H:%M:%S %B %d, %Y")

        body = {'values': [['Updated On', '{}'.format(now)]]}

        return self.client.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            range="{}!{}".format(self.sheet_name, 'A3'),
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()

    # Loads spredsheet data into list of dicts 
    def from_sheet_data(self, data, indexField=None):
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

    # Converts list of dicts into sheet compatible format
    def to_sheet_data(self, rows, skip_labels=False):
        data = []
        column_labels = []
        for row in rows:
            for k, v in row.items():
                if k not in column_labels:
                    column_labels.append(k)

            current_row = [''] * (max(len(column_labels), len(row.keys())))

            for k, v in row.items():
                idx = column_labels.index(k)
                if isinstance(v, datetime.date):
                    v = v.strftime("%m/%d/%Y")
                current_row[idx] = v

            data.append(current_row)

        if skip_labels:
            return data
        return [column_labels] + data


# Updates the sheet with the format specified in the function
def format_sheet():
    # Helper functions to make declaring the format a little less 
    # stress-inducing

    # Returns a dict with keys 'sheetId', 'startRowIndex', 'endRowIndex',
    # 'startColumnIndex', and 'endColumnIndex'. If any of the paramters are None,
    # the key is not included in the final dict.
    def sheetRange(id, r_start, r_end, c_start, c_end):
        output = {}
        if id is not None: output['sheetId'] = id
        if r_start is not None: output['startRowIndex'] = r_start
        if r_end is not None: output['endRowIndex'] = r_end
        if c_start is not None: output['startColumnIndex'] = c_start
        if c_end is not None: output['endColumnIndex'] = c_end
        return output

    # Returns a dict with key 'backgroundColor' set to the rgb values in the 
    # params
    def backgroundColor(r, g, b):
        return {'backgroundColor': {'red': r, 'green': g, 'blue': b}}

    # Returns a dict with key 'textFormat' set to the values in the params
    def textFormat(size, bold):
        return {'textFormat': {'fontSize': size, 'bold': bold}}

    # Returns a dict with key 'numberFormat' set to the values in the params
    def numberFormat(type, pattern):
        return {'numberFormat': {'type': type, 'pattern': pattern}}

    client = GoogleSheetClient()

    request_body = {
        'requests': [
            # All Instances
            {
                'repeatCell': {
                    'range': sheetRange(0, 3, 4, 0, 10),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(117, 59, 25),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
            {
                'repeatCell': {
                    'range': sheetRange(0, 2, 3, 0, 2),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(19, 75, 219),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                },
            },

            # All cluster Instances
            {
                'repeatCell': {
                    'range': sheetRange(1587125586, 3, 4, 0, 10),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(117, 59, 25),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
            {
                'repeatCell': {
                    'range': sheetRange(1587125586, 2, 3, 0, 2),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(19, 75, 219),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                },
            },

            # Cost Summary
            {
                'repeatCell': {
                    'range': sheetRange(1239517681, 2, 3, 0, 2),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(19, 75, 219),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
            {
                'repeatCell': {
                    'range': sheetRange(1239517681, 3, 4, 0, 2),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(117, 59, 25),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
            {
                'repeatCell': {
                    'range': sheetRange(1239517681, 4, None, 1, 2),
                    'cell': {
                        'userEnteredFormat': {
                            **numberFormat('CURRENCY', '$#,##.00'),
                            **textFormat(11, True)
                        }
                    },
                    'fields': 'userEnteredFormat(numberFormat,textFormat)'
                }
            },

            # Instances cost
            {
                'repeatCell': {
                    'range': sheetRange(755432813, 2, 3, 0, 2),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(19, 75, 219),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
            {
                'repeatCell': {
                    'range': sheetRange(755432813, 3, 4, 0, 11),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(117, 59, 25),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
            {
                'repeatCell': {
                    'range': sheetRange(755432813, 4, None, 10, 11),
                    'cell': {
                        'userEnteredFormat': {
                            **numberFormat('CURRENCY', '$#,##.00'),
                            **textFormat(11, True)
                        }
                    },
                    'fields': 'userEnteredFormat(numberFormat,textFormat)'
                }
            },

            # Old Clusters
            {
                'repeatCell': {
                    'range': sheetRange(42437603, 2, 3, 0, 2),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(19, 75, 219),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
            {
                'repeatCell': {
                    'range': sheetRange(42437603, 3, 4, 0, 6),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(117, 59, 25),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },

            # All Clusters
            {
                'repeatCell': {
                    'range': sheetRange(846402724, 2, 3, 0, 2),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(19, 75, 219),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
            {
                'repeatCell': {
                    'range': sheetRange(846402724, 3, 4, 0, 5),
                    'cell': {
                        'userEnteredFormat': {
                            **backgroundColor(117, 59, 25),
                            **textFormat(12, True)
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            }
        ]
    }

    response = client.service.spreadsheets().batchUpdate(
        spreadsheetId=os.getenv('GOOGLE_SHEET_ID'),
        body=request_body
    ).execute()
