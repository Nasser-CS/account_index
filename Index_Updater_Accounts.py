##Load relevant libraries
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from functools import reduce
import fuzzywuzzy

##Load relevant data sources
index = pd.read_csv(r'C:\Users\', encoding='latin-1', low_memory=False)
vmw = pd.read_csv(r'C:\Users\', encoding='latin-1', low_memory=False)
sbu = pd.read_csv(r'C:\Users\', encoding='latin-1', low_memory=False)
indicators = pd.read_csv(r'C:\Users\', encoding='latin-1', low_memory=False)

##Rename merging columns
vmw = vmw.rename(columns={'VMW_ACCT_ID': 'VMW_ACCT_ID'})
sbu = sbu.rename(columns={'Account #': 'CB_ACCT_ID'})

sbu = sbu.rename(columns={'D&B DUNS Number': 'DUNS'})
indicators = indicators.rename(columns={'D-U-N-S Number': 'DUNS_x'})

##DUNS needs to remain int, not convert to str, to preserve the rc in merge.
sbu.DUNS = sbu.DUNS.fillna(0.0).astype(int)
#accounts = pd.merge(left=index, right=sbu, how='left', left_on='VMW_ACCT_ID', right_on='VMW_ACCT_ID')

updated_all_sbu = sbu.merge(index.drop_duplicates('CB_ACCT_ID'),on='CB_ACCT_ID',how='left').merge(vmw,on='VMW_ACCT_ID',how='left')
updated_all_sbu = updated_all_sbu.merge(indicators,on='DUNS_x')
#import time

#TodaysDate = time.strftime("%d-%m-%Y")
#excelfilename = "Index_Refresh"

updated_all_sbu.to_csv (r'', index = None, header=True)

# Fields to generate (Line of Business	Account #	Account Name	Sales Account Manager	Type	Classification	Type	Mapped	APPD	CS Customer	ELA Value	ELA Date)
# VMS_Map = CB_Accounts
# VMS_Map['VMW'] = ""
# VMS_Map['VMW_ACCT_ID'] = VMS_Map.Account_ID.map(Index.set_index('CB_ACCT_ID')['VMW_ACCT_ID'].to_dict())


## Filter just to mapped accounts and create all flags
updated_all_sbu = updated_all_sbu.rename(columns={'Sales Classification': 'classification'})


## Pretty Tables
pd.options.display.width = 0
from tabulate import tabulate

print(tabulate(updated_all_sbu, headers='firstrow', tablefmt='github'))
print updated_all_sbu

updated_all_sbu['mapped'] = pd.np.where(updated_all_sbu.VMW_ACCT_ID.str.contains(""), "Yes","No")

updated_all_sbu.fillna(0,inplace=True)
updated_all_sbu.sort_values(['Mapped','Line of Business'], ascending=False )
updated_all_sbu.to_html('temp.html')



## Remove Whitespace
updated_all_sbu['classification'] = updated_all_sbu['classification'].str.strip()

updated_all_sbu['E1'] = pd.np.where(updated_all_sbu.classification.str.contains("E1"), "1","0")
updated_all_sbu['E2'] = pd.np.where(updated_all_sbu.classification.str.contains("E2"), "1","0")
updated_all_sbu['C1'] = pd.np.where(updated_all_sbu.classification.str.contains("C1"), "1","0")
updated_all_sbu['C2'] = pd.np.where(updated_all_sbu.classification.str.contains("C2"), "1","0")

updated_all_sbu['mapped'] = pd.np.where(updated_all_sbu.VMW_ACCT_ID.str.contains(""), "1","0")
updated_all_sbu.loc[updated_all_sbu['Employees'] > 5, 'employee_cutoff'] = '1'
updated_all_sbu.loc[(updated_all_sbu['Line of Business'] == 'AMER Inside') & (updated_all_sbu['employee_cutoff'] == '1'), 'inside_employee_flag'] = '1'



updated_all_sbu.loc[(updated_all_sbu['Line of Business'] == '') & (updated_all_sbu['E2'] == 'E2'), 'inside_e2'] = '1'  
updated_all_sbu.loc[(updated_all_sbu['Line of Business'] == '') & (updated_all_sbu['E1'] == 'E1'), 'inside_e1'] = '1'  


##Load Territories (Field and Inside)
Inside = pd.read_excel(r'C:', sheet_name='Sheet1')
Field = pd.read_excel(r'C:', sheet_name='VMW Territory')

Field = Field.rename(columns={'Rep Name': 'rep'})
Inside = Inside.rename(columns={'Rep': 'rep'})
updated_all_sbu = updated_all_sbu.rename(columns={'Sales Account Manager': 'account_manager'})

LATAM = pd.read_excel(r'', sheet_name='sbu_latam_mapping')
LATAM['LATAM'].str.lower()
LATAM['Carribean'].str.lower()
updated_all_sbu[''].str.lower()

##Map In New Territory Fields

updated_all_sbu = pd.read_csv(r'', encoding='latin-1', low_memory=False)
 
updated_all_sbu['new_rep'] = updated_all_sbu.account_manager.map(Field.set_index('rep')['VMW ID'].to_dict())
updated_all_sbu['new_sales_assignment'] = updated_all_sbu.account_manager.map(Field.set_index('rep')['Sales Assignment'].to_dict())
updated_all_sbu['new_territory'] = updated_all_sbu.account_manager.map(Field.set_index('rep')['Territory Name'].to_dict())

##Export
updated_all_sbu.to_csv (r'', index = None, header=True)




## Logic Engine
## Field
df.loc[df['column_name'] == some_value]

## Inside
df.loc[df['column_name'] == some_value]

## EMEA / APJ
df.loc[df['column_name'].isin(some_values)]