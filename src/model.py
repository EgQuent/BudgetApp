import pandas as pd
import os.path
import json

class Reader:

    AKEY = 'Montant'

    def __init__(self, file):
        self.file = os.path.join(os.getcwd(), file)

    def open_file(self):
        return self._with_file()
    
    def save_file(self, data):
        self._with_file(data)

    def _with_file(self, data = None):
        if self.file:
            try:
                if data:
                    self._sub_save_file(data)
                else:
                    return self._sub_open_file()
            except ValueError:
                print("File cannot be opened or saved.")
            except FileNotFoundError:
                print("File not found.")
            except:
                print("Unknown error.")

    def _sub_open_file(self):
        if self.file.endswith('csv'):
            return self._open_csv()
        elif self.file.endswith('json'):
            return self._open_json()

    def _sub_save_file(self, data):
        if self.file.endswith('csv'):
            self._save_csv(data)
        elif self.file.endswith('json'):
            self._save_json(data)


    def _open_csv(self):
        try :
            df = pd.read_csv(self.file, sep=';')
            if self.AKEY in  df.head() :
                for ind in df.index:
                    try: 
                        df.at[ind, self.AKEY] = float(df.at[ind, self.AKEY] )
                    except ValueError:
                        no_space = df.at[ind, self.AKEY].replace(' ','')
                        no_comma = no_space.replace(',','.')
                        df.at[ind, self.AKEY] = float(no_comma) 
        except :
            print("Cannot parse this CSV file.")
            return None
        return df

    def _open_json(self):
        try:
            with open(self.file, 'r') as json_file:
                return json.load(json_file)
        except :
            print("Cannot parse this JSON file.")

    def _save_csv(self, data):
        data.to_csv(self.file, sep=";", index=False)
    
    def _save_json(self, data):
        with open(self.file, 'w') as json_file:
            json.dump(data, json_file)

class BasicModel():

    KEYS = ['Incomes, Savings, Cars']

    def __init__(self, file):
        self.file = file
        self.data = Reader(self.file).open_file()
        self._check_data()
        self.incomes_table = self._load(self.data, 'Incomes')
        self.savings_table = self._load(self.data, 'Savings')
        self.cars = list(self.data['Cars'].keys())
        self.cars_tables = self._load_cars()

    def _check_data(self):
        for key in self.KEYS:
            if not key in self.data.keys():
                self.data[key] = {}

    @staticmethod
    def _load(_dict, key, file_name='file'):
        try:
            return Reader(_dict[key][file_name]).open_file()
        except KeyError as error:
            print(f"Error parsing dict : {error}")

    def _load_cars(self):
        if self.cars:
            tables = {}
            for car in self.cars:
                tables[car] = {}
                tables[car]['cost'] = self._load(self.data['Cars'], car, 'cost_file')
                tables[car]['kms'] = self._load(self.data['Cars'], car, 'km_file')
            return tables




    
