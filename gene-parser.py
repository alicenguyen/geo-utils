import csv
import glob
import gzip
from collections import defaultdict

DATA_FILEPATH = 'sample_data/*.txt.gz'
TRANSCRIPT_ID_COL_IDX = 0
TRANSCRIPT_ABUNDANCE_COL_IDX = 8

overall_set_collection = defaultdict(list)
sampled_transcripts_collection = defaultdict(dict)
unique_sample_names = []

def extract_sample_name(string):
    tokens = string.split('_')  # todo improve this
    return tokens[2] + '_' + tokens[3]

for file_name in glob.glob(DATA_FILEPATH):
    print 'processing ' + file_name
    sample_name = extract_sample_name(file_name)
    unique_sample_names.append(sample_name)

    with gzip.open(file_name, 'rb') as in_file:
        reader = csv.reader(in_file, delimiter='\t')
        next(reader, None)  # skip  the header row

        for line in [l for l in reader if l[1] != '-']:
            gene_id = line[TRANSCRIPT_ID_COL_IDX]
            abundance = line[TRANSCRIPT_ABUNDANCE_COL_IDX]
            sampled_transcripts_collection[gene_id][sample_name] = abundance

with open('test.csv', 'wb') as outfile:
    field_names = ['transcript_id'] + sorted(unique_sample_names)
    writer = csv.DictWriter(outfile, fieldnames=field_names)

    writer.writeheader()
    for transcript_id, t_dict in sorted(sampled_transcripts_collection.items()):
        row_dict = {'transcript_id': transcript_id}
        for sample_key in sorted(unique_sample_names):
            row_dict[sample_key] = t_dict.get(sample_key, 0)
        writer.writerow(row_dict)
