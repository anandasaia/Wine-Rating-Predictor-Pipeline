import luigi
import os
from pathlib import Path

from util import DockerTask

VERSION = os.getenv('PIPELINE_VERSION', '0.1')


class Debug(DockerTask):
    """Use this task with appropriate image to debug things."""

    @property
    def image(self):
        return f'code-challenge/download-data:{VERSION}'

    @property
    def command(self):
        return [
            'sleep', '3600'
        ]

#Download
class DownloadData(DockerTask):
    """Initial pipeline task downloads dataset."""

    fname = luigi.Parameter(default='wine_dataset')
    out_dir = luigi.Parameter(default='/usr/share/data/raw/')
    url = luigi.Parameter(
        default='https://github.com/datarevenue-berlin/code-challenge-2019/'
                'releases/download/0.1.0/dataset_sampled.csv'
    )

    @property
    def image(self):
        return f'code-challenge/download-data:{VERSION}'

    @property
    def command(self):
        return [
            'python', 'download_data.py',
            '--name', self.fname,
            '--url', self.url,
            '--out-dir', self.out_dir
        ]

    def output(self):
        out_dir = Path(self.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        return luigi.LocalTarget(
            path=str(out_dir/f'{self.fname}.csv')
        )
        #Cleaning
class CleanData(DockerTask):
    """Task to clean the dataset"""

    in_path = '/usr/share/data/raw/'
    in_csv = luigi.Parameter(default= in_path + 'wine_dataset.csv')
    out_dir = luigi.Parameter(default='/usr/share/data/created_csv/')
    flag = luigi.Parameter('.SUCCESS_CleanData')

    @property
    def image(self):
        return f'code-challenge/clean-data:{VERSION}'

    def requires(self):
        return DownloadData()

    @property
    def command(self):
        return [
            'python', 'clean_data.py',
            '--in-csv', self.in_csv,
            '--out-dir', self.out_dir,
            '--flag', self.flag
        ]

    def output(self):
        return luigi.LocalTarget(
            #path=str(out_dir/f'cleaned.csv')
            path=str(Path(self.out_dir) / self.flag)
        )
        
#Transform
class TransformData(DockerTask):
    """Task to simplify datasets"""

    in_path = '/usr/share/data/created_csv/'
    in_csv = luigi.Parameter(default= in_path + 'cleaned.csv')
    out_dir = luigi.Parameter(default=in_path)
    flag = luigi.Parameter('.SUCCESS_TransformData')
    @property
    def image(self):
        return f'code-challenge/transform-data:{VERSION}'

    def requires(self):
        return CleanData()

    @property
    def command(self):
        return [
            'python', 'transform_data.py',
            '--in-csv', self.in_csv,
            '--out-dir', self.out_dir,
            '--flag', self.flag
        ]

    def output(self):
        return luigi.LocalTarget(
            path=str(Path(self.out_dir) / self.flag)
        )
 
        
        
#Train

class BuildModel(DockerTask):
    """Task to train random forest classifier with datasets and evaluate the predictions"""

    in_path = '/usr/share/data/created_csv/'
    train_csv = luigi.Parameter(default= in_path + 'transformed.csv')
    out_dir = luigi.Parameter(default='/usr/share/data/output/')

    @property
    def image(self):
        return f'code-challenge/build-model:{VERSION}'

    def requires(self):
        return TransformData()

    @property
    def command(self):
        return [
            'python', 'build_model.py',
            '--train-csv', self.train_csv,
            '--out-dir', self.out_dir
        ]

    def output(self):
        return luigi.LocalTarget(
            path=str(Path(self.out_dir) / 'model.sav')
        )

