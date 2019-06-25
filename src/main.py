from pyspark.sql import *
import pyspark.sql.functions as f
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, Tokenizer, NGram, HashingTF, MinHashLSH

from itertools import combinations
from termcolor import colored
#from datasketch import MinHash
from io import BytesIO

import boto3
import pretty_midi
import min_hash
import os
import sys

#s3_bucket = 'midi-files-partial'
s3_bucket = 'midi-files-sample1'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/config")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/lib")
import config
import locality_sensitive_hash
import util

#Define Spark Configuration
def spark_conf():
    conf = SparkConf().setAppName("processMIDIfiles")
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.getOrCreate()
    return spark

spark = spark_conf()

def write_df_to_pgsql(df, table_name):
    postgresql_user = os.environ.get('POSTGRESQL_USER')
    postgresql_password = os.environ.get('POSTGRESQL_PWD')
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://10.0.0.13:2762/lmd") \
        .option("dbtable", table_name) \
        .option("user", postgresql_user) \
        .option("password", postgresql_password) \
        .save()

def process_df(df):
    model = Pipeline(stages = [RegexTokenizer(pattern = " ", inputCol = "instruments", outputCol = "instruments_tokenized", minTokenLength = 1),
                           NGram(n = 1, inputCol = "instruments_tokenized", outputCol = "instruments_ngrams"),
                           HashingTF(inputCol = "instruments_ngrams", outputCol = "instruments_vectors"),
                           MinHashLSH(inputCol = "instruments_vectors", outputCol = "instruments_lsh", numHashTables = 10)]).fit(df)

    df_hashed = model.transform(df)
    #df_hashed.show(15)
    df_matches = model.stages[-1].approxSimilarityJoin(df_hashed, df_hashed, 0.5, distCol="JaccardDistance").select(
                f.col('datasetA.filename').alias('filename_A'),
                f.col('datasetB.filename').alias('filename_B'),
                f.col('JaccardDistance'))
    #df_matches.show(15)
    write_df_to_pgsql(df_matches, 'filepair_similarity5')

#Read all MIDI files from S3 bucket
def read_midi_files():
    invalid_files = []
    number_of_files = 0
    number_of_valid_files = 0
    filename_instruments_seq = []

    #Set s3-boto config
    s3 = boto3.resource('s3')
    boto_client = boto3.client('s3')
    bucket = s3.Bucket(s3_bucket)

    #DataFrame schema
    File_Instruments = Row("filename", "instruments")
    filename_instruments_seq = []

    for obj in bucket.objects.all():
        number_of_files+=1
        s3_key = obj.key
        midi_obj_stream = boto_client.get_object(Bucket=s3_bucket, Key=s3_key)
        midi_obj = BytesIO(midi_obj_stream['Body'].read())
        try:
            pretty_midi_obj = pretty_midi.PrettyMIDI(midi_obj)
            number_of_valid_files+=1
            filename = s3_key
            instruments_list = list(map(lambda x: str(x.program), pretty_midi_obj.instruments))
            instruments_list_set = set(instruments_list)
            instruments_list_uniq = list(instruments_list_set)
            instruments = " ".join(instruments_list_uniq)
            if(len(instruments_list_uniq) >=3):
                filename_instruments_seq.append(File_Instruments(filename,instruments))
        except:
            invalid_files.append(s3_key)
    df_song_instrument = spark.createDataFrame(filename_instruments_seq)
    process_df(df_song_instrument)

if __name__ == '__main__':
    read_midi_files()
