import pandas as pd
import os.path
import json

class Reader:

    AKEY = 'Montant'

    def __init__(self, file):
        self.file = os.path.join(os.getcwd(), file)
        self.data = None

    def open_file(self):
        self.with_file(False)
    
    def save_file(self):
        self.with_file(True)

    def with_file(self, to_save = True):
        if self.file:
            try:
                if to_save:
                    self.sub_save_file()
                else:
                    self.sub_open_file()
            except ValueError:
                print("File cannot be opened or saved.")
            except FileNotFoundError:
                print("File not found.")
            except:
                print("Unknown error.")

    def sub_open_file(self):
        if self.file.endswith('csv'):
            self.open_csv()
        elif self.file.endswith('json'):
            self.open_json()

    def sub_save_file(self):
        if self.data is not None:
            if self.file.endswith('csv'):
                self.df = self.data
                self.save_csv()
            elif self.file.endswith('json'):
                self.json = self.data
                self.save_json()


    def open_csv(self):
        df = pd.read_csv(self.file, sep=';')
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
        self.data = df

    def open_json(self):
        try:
            with open(self.file, 'r') as json_file:
                self.data = json.load(json_file)
        except :
            print("Cannot parse this JSON file.")

    def save_csv(self):
        self.data.to_csv(self.file, sep=";", index=False)
    
    def save_json(self):
        with open(self.file, 'r') as json_file:
            json.dump(self.data, json_file)

class BasicModel(Reader):
    def __init__(self, file):
        super().__init__(file)
        self.df = None
        self.json = None

    
