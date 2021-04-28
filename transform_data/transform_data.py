
import pandas as pd
import numpy as np
import click
from pathlib import Path

#Function definition to save transformed data as new csv file
def _save_datasets(dp, outdir: Path, flag):
    out_trans = outdir / 'transformed.csv/'
    flag = outdir / flag
    dp.to_csv(out_trans)
    flag.touch()

def transform_points_simplified(points):
    if points < 85:
        return 1
    elif points >= 85 and points < 90:
        return 2 
    elif points >= 90 and points < 95:
        return 3 
    elif points >= 95 and points < 100:
        return 4 
    else:
        return 5
        
@click.command()
@click.option('--in-csv')
@click.option('--out-dir')
@click.option('--flag')
def transform_data(in_csv,out_dir, flag):
    out_dir = Path(out_dir)
    #selecting required coloumns to be used for simplified model
    col_list=['description', 'points']
    dp=pd.read_csv(in_csv, usecols=col_list)
    #transforming based on the definition of transform_points_simplified()
    dp = dp.assign(points_simplified = dp['points'].apply(transform_points_simplified))
    #function call to save data as new csv
    _save_datasets(dp,out_dir, flag)
    

if __name__ == "__main__":
   transform_data()  

