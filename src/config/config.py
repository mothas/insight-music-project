import os

# Program settings
SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DEBUG = True

# MinHash, LSH parameters
MIN_HASH_K_VALUE = 0
LSH_NUM_BANDS = 0
LSH_BAND_WIDTH = 0
LSH_NUM_BUCKETS = 0
LSH_SIMILARITY_BAND_COUNT = 0  # Number of common bands needed for MinHash comparison

# Dump files to synchronize models across spark streaming/batch
MIN_HASH_PICKLE = SRC_PATH + "/lib/mh.pickle"
LSH_PICKLE = SRC_PATH + "/lib/lsh.pickle"
