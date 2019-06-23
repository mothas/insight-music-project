from pyspark.sql import *
from pyspark import SparkConf
from pyspark import SparkContext

from itertools import combinations
from datasketch import MinHash
from io import BytesIO

import boto3
import pretty_midi
import os

s3_bucket = 'midi-files-partial'

#Define Spark Configuration
def spark_conf():
    conf = SparkConf().setAppName("processMIDIfiles")
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.getOrCreate()
    return spark

spark = spark_conf()

#Read all MIDI files from S3 bucket
def read_midi_files():
    invalid_files = []
    number_of_files = 0
    number_of_valid_files = 0
    filename_instruments_dict = {}

    #Set s3-boto config
    s3 = boto3.resource('s3')
    boto_client = boto3.client('s3')
    bucket = s3.Bucket(s3_bucket)

    #DataFrame schema
    File_Instruments = Row("filename", "instruments")
    filename_instruments_seq = []
    filenames = []

    for obj in bucket.objects.all():
        number_of_files+=1
        s3_key = obj.key
        midi_obj_stream = boto_client.get_object(Bucket=s3_bucket, Key=s3_key)
        midi_obj = BytesIO(midi_obj_stream['Body'].read())
        try:
            pretty_midi_obj = pretty_midi.PrettyMIDI(midi_obj)
            number_of_valid_files+=1
            filename = s3_key
            instruments = list(map(lambda x: str(x.program), pretty_midi_obj.instruments))
            filename_instruments_dict[filename] = instruments
            filenames.append(filename)
        except:
            invalid_files.append(s3_key)
    #df_song_instrument = spark.createDataFrame(filename_instruments_seq)
    #print('!!!!! COUNT 1 !!!!! ', df_song_instrument.count())
    print('!!!!! COUNT 1 !!!!! ', len(filenames))
    print('!!!!! COUNT 2 !!!!! ', len(invalid_files))

    create_pair_midifiles(filenames, filename_instruments_dict)

def create_pair_midifiles(filenames, filename_instruments_dict):
    #FilePair_Score = Row("filename1","filename2","score")
    #print('filename_instruments_dict', filename_instruments_dict)
    filename_pairs = list(combinations(filenames,2))
    print('!!!! filename_pairs', len(filename_pairs))
    for pair in filename_pairs:
        #print('!!!! pair', pair)
        filename1, filename2 = pair[0], pair[1]
        filename1_mh, filename2_mh = MinHash(), MinHash()
        instruments1 = filename_instruments_dict[filename1]
        instruments2 = filename_instruments_dict[filename2]
        for ins1 in instruments1:
            filename1_mh.update(str(ins1).encode('utf8'))
        for ins2 in instruments2:
            filename2_mh.update(str(ins2).encode('utf8'))

        minhash_similarity = filename1_mh.jaccard(filename2_mh)
        s1 = set(instruments1)
        s2 = set(instruments2)
        jaccard_similarity = float(len(s1.intersection(s2)))/float(len(s1.union(s2)))

        print(filename1,filename2,minhash_similarity,jaccard_similarity)


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

if __name__ == '__main__':
    read_midi_files()
