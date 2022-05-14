import os
import pandas as pd
import numpy as np
import ntpath
import time
import inspect
import shutil

from ml_experiments.enums import DatasetState
from loguru import logger

class Dataset:
    def __init__(self, dataset_path, csv_path, output_directory, output_format):

        self._split_state = DatasetState.SPLIT_INIT
        self._split_method = None

        self._date_format = "%Y-%m-%d_%H%M"

        self.dataset_path = dataset_path
        self.csv_path = csv_path
        self.dataset_classes = None

        self.csv_extension = ['csv']
        self.image_extensions = ["png", "jpeg", "jpg"]

        # Define the output dir based on the required format
        if(output_format == "df"):
            self.output_directory = None
        elif (output_format == "directory"):
            self.output_directory = f'{output_directory}_{time.strftime(self._date_format, time.gmtime())}'
        else:
            raise Exception("Output format not supported. Can only convert the dataset to either dataframe or directory")

        # Call it to validate the given arguments
        self._validate_arguments()

    @property
    def split_state(self):
        return self._split_state

    @split_state.setter
    def split_state(self, value):
        self._split_state = value

    @property
    def split_method(self):
        return self._split_method

    @split_method.setter
    def split_method(self, value):
        self._split_method = value

    def _validate_arguments(self):
        if not os.path.isdir(self.dataset_path):
            raise Exception(f"Dataset input directory {self.dataset_path} does not exist...")
        
        if not os.path.isfile(self.csv_path) \
            and not os.access(self.csv_path, os.R_OK):
            raise Exception(f"Either the CSV file {self.csv_path} is missing or not readable...")

        if not self._allowed_extenstion(self._path_leaf(self.csv_path), self.csv_extension):
            raise Exception(f"Dataset {self._path_leaf(self.csv_path)} file must be in .csv format...")

        if self.output_directory and  not os.path.isdir(self.output_directory):
            logger.info(f'Dataset output directory {self.output_directory} does not exist, creating a new directory {self.output_directory}...')
            os.makedirs(self.output_directory, exist_ok=True)

    def _allowed_extenstion(self, filename, allowed_extension):
        file_name = filename.lower()
        return "." in file_name and file_name.rsplit('.', 1)[1].lower() in allowed_extension

    def _path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def get_classes(self):
        if self.split_state is not DatasetState.SPLIT_END:
            logger.error(f"You must split the dataset first before calling {inspect.stack()[0][3]}")
            return

        if self.output_directory is not None and self.split_method is DatasetState.SPLIT_DIR:
            classes = os.listdir(self.output_directory)
            logger.info(classes)
            return classes

        if self.split_method is DatasetState.SPLIT_DF:
            raise NotImplementedError

    def get_report(self):
        raise NotImplementedError

    def split_to_df(self):
        # self.split_method = DatasetState.SPLIT_DF
        # self.split_state = DatasetState.SPLIT_END
        raise NotImplementedError

    def split_to_directory(self):
        self.split_method = DatasetState.SPLIT_DIR
        df = pd.read_csv(self.csv_path)
        df_header = list(df)

        # Validate that the datafrate contains image_id and label as headers
        if not all(x in df_header for x in ['image_id', 'label']):
            logger.error(f'CSV file missing {"image_id, label"} headers. Aborting splitting..')
            return

        self.dataset_classes = df['label'].unique()

        # Create folders for each label in the datast directory
        for label in self.dataset_classes:
            if not os.path.exists(os.path.join(self.output_directory, label)):
                os.mkdir(os.path.join(self.output_directory, label))

        # Get the images from the dataset directory, match them with the csv, and move them to directories
        df_copy = df.copy()
        df_copy.reset_index()
        for idx, img in df.iterrows():
            shutil.copy2(
                os.path.join(self.dataset_path, img['image_id']), 
                os.path.join(self.output_directory, img['label']))

        self.split_state = DatasetState.SPLIT_END
        logger.info(f"Dataset splitted to {self.output_directory} successfully.")
