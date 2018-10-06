import os
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Change if different for your environment
DATASET_DIR = os.path.join(ROOT_DIR, 'Datasets')

# Change if different for your environment
DATABASE_DIR = os.path.join(os.path.dirname(__file__), 'Database')

logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO,
                    filename=os.path.join(ROOT_DIR, 'log'))
logging.getLogger().addHandler(logging.StreamHandler())
