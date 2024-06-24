import os
import pandas as pd
import datetime
import numpy as np

class Processor:
    def __init__(self, files):
        self.turnouts = self.produce_turnouts_table(files)
        self.elections = self.produce_elections_tables(files)
        
    def produce_elections_tables(self, files):
        # create a dict to hold each of the election dataframes
        elections = dict()
        
        for f in files:
            # get the name of the file
            filename = os.path.basename(f)
            
            # read the xls file
            temp_df = pd.read_excel(f, engine='xlrd', sheet_name=None)
            
            # get only the election breakdown pages
            #df = pd.concat(list(temp_df.values())[2:], ignore_index=True)
            temp_df.pop('Table of Contents')
            temp_df.pop('Registered Voters')
            
            # go through each race in this file
            keys = list(temp_df.keys())
            for k in keys:
                page = temp_df.pop(k)
                
                # get the name of the race
                race = page.columns[0]
                
                # reset the columns
                page.columns = page.iloc[1]
                page.columns.name = None
                
                # remove the leading two rows in the df
                page = pd.DataFrame(page[2:])
                page = page.reset_index(drop=True)
                
                # set the value with an updated key
                temp_df[race] = page
            
            # add this df to the dict of dataframes
            #elections[filename] = df
            elections[filename] = temp_df
        
        return elections
        
    def produce_elections_table(self, file):
        # create a blank dataframe
        df = pd.DataFrame()
        
        # get the name of the file
        filename = os.path.basename(file)
        
        # read the xls file
        temp_df = pd.read_excel(file, engine='xlrd', sheet_name=None, skiprows=[0])
        temp_df['Filename'] = filename
        
        df = pd.concat(list(temp_df.values())[2:], ignore_index=True)
        
        return df
    
    def produce_turnouts_table(self, files):
        # create a blank dataframe
        df = pd.DataFrame()
        
        for f in files:
            # get the name of the file
            filename = os.path.basename(f)
            
            # read the xls file
            temp_df = pd.read_excel(f, engine='xlrd', sheet_name='Registered Voters')
            temp_df['Filename'] = filename
            
            if len(df) < 1:
                df = temp_df
                #df = pd.concat(list(temp_df.values())[0:], ignore_index=True)
            else:
                concat = pd.concat([df, temp_df], axis=0, ignore_index=True)
                df = concat
        
        return df
        
    def get_elections_tables(self):
        return self.elections
    
    def get_turnouts_table(self):
        return self.turnouts
        
    
if __name__ == "__main__":
    processor = Processor(['hd32_special23_detail.xls', 'allegheny_general23_detail.xls', 'allegheny_general22_detail.xls', 'allegheny_primary24_detail.xls'])
    print("-------------- Turnouts Table ---------------")
    print(processor.get_turnouts_table().head(10))
    print(processor.get_turnouts_table().tail(10))
    print()
    #print("-------------- Elections Table ---------------")
    #print(processor.get_elections_table().head(10))
    #print()