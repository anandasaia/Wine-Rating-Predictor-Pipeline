
import pandas as pd
import numpy as np
import click
from pathlib import Path

# Function to Save Cleaned Data as CSV file
def _save_datasets(clean, outdir: Path, flag):
    out_clean = outdir / 'cleaned.csv/'
    flag = outdir / flag
    clean.to_csv(str(out_clean), index=False)
     # save as csv and create flag file
    flag.touch()


    
@click.command()
@click.option('--in-csv')
@click.option('--out-dir')
@click.option('--flag')
def clean_data(in_csv,out_dir, flag):

    out_dir = Path(out_dir)
   #removing duplicates and Nan Value    
    data=pd.read_csv(in_csv)   
    clean= data[data.duplicated('description', keep=False)]
    clean.dropna(subset=['description', 'points'])
   #Saving the duplicates removed file as new csv
    _save_datasets(clean,out_dir, flag)

if __name__ == "__main__":
    clean_data()
  


  
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
