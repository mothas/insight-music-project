from io import BytesIO
import boto3
import pretty_midi

s3 = boto3.resource('s3')
boto_client = boto3.client('s3')

bucket = s3.Bucket('midi-files-partial')

invalid_files = []

for obj in bucket.objects.all():
    s3_key = obj.key
    midi_obj_stream = boto_client.get_object(Bucket='midi-files-partial',Key=s3_key)
    try:
        midi_obj = BytesIO(midi_obj_stream['Body'].read())
        pretty_midi_obj = pretty_midi.PrettyMIDI(midi_obj)
        print('Number of instruments: ', len(pretty_midi_obj.instruments))
    except:
        invalid_files.append(s3_key)
