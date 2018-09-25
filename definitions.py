import os
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(ROOT_DIR, 'Datasets')

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO,
                    filename=os.path.join(ROOT_DIR, 'log'))
logging.getLogger().addHandler(logging.StreamHandler())
