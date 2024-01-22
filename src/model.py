import pandas as pd
import os.path
import json


class BasicModel:
    def __init__(self, file):
        self.file = os.path.join( os.getcwd(), file)
        self.df = None
        self.json = None

    def open_file(self):
        if self.file:
            try:
                if self.file.endswith('csv'):
                    self.open_csv()
                elif self.file.endswith('json'):
                    self.open_json()
            except ValueError:
                print("File cannot be opened.")
            except FileNotFoundError:
                print("File not found.")
            except:
                print("Unknown error.")

    def save_file(self, data=None):
        if self.file:
            try:
                if self.file.endswith('csv'):
                    if data is not None:
                        self.df = data
                    self.save_csv()
                elif self.file.endswith('json'):
                    if data :
                        self.json = data
                    self.save_json()
            except ValueError:
                print("File cannot be saved.")
            except FileNotFoundError:
                print("File not found.")
            except:
                print("Unknown error.")

    def open_csv(self):
        self.df = pd.read_csv(self.file, sep=';')
        for ind in self.df.index:
            try: 
                self.df.at[ind, 'Montant'] = float(self.df.at[ind, 'Montant'] )
            except:
                no_space = self.df.at[ind, 'Montant'].replace(' ','')
                no_comma = no_space.replace(',','.')
                self.df.at[ind, 'Montant'] = float(no_comma)

    def open_json(self):
        with open(self.file, 'r') as json_file:
            self.json = json.load(json_file)

    def save_csv(self):
        self.df.to_csv(self.file, sep=";", index=False)
    
    def save_json(self):
        pass
