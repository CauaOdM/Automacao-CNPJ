import pandas as pd

class ReadExcel:
    def __init__(self, path):
        self.path = path
        self.df = pd.read_excel(self.path)

    def list_cnpj(self):
        cnpjs = self.df['CNPJ'].to_list()
        return cnpjs