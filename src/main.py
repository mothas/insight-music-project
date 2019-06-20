from io import BytesIO
from pyspark.sql import *
import boto3
import pretty_midi

s3 = boto3.resource('s3')
boto_client = boto3.client('s3')

s3_bucket = 'midi-files-partial'
bucket = s3.Bucket(s3_bucket)

invalid_files = []
number_of_files = 0
number_of_valid_files = 0
number_of_invalid_files = 0
number_of_song_instruments = 0

#Define Spark Configuration
def spark_conf():
    conf = SparkConf().setAppName("processMIDIfiles")
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.getOrCreate()
    return spark

Song_Instrument = Row("filename", "instrument")
song_instrument_seq = []

#Read all MIDI files from S3 bucket
for obj in bucket.objects.all():
    number_of_files+=1
    s3_key = obj.key
    midi_obj_stream = boto_client.get_object(Bucket=s3_bucket, Key=s3_key)
    midi_obj = BytesIO(midi_obj_stream['Body'].read())
    try:
        pretty_midi_obj = pretty_midi.PrettyMIDI(midi_obj)
        number_of_song_instruments += len(pretty_midi_obj.instruments)
        number_of_valid_files+=1
        for ins in pretty_midi_obj.instruments:
            song_instrument_seq.append(Song_Instrument(s3_key,ins))
    except:
        invalid_files.append(s3_key)
        number_of_invalid_files+=1

df_song_instrument = spark.createDataFrame(song_instrument_seq)

print('!!! COUNT: ', df_song_instrument.count())
