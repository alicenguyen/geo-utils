import csv
import glob
from collections import defaultdict


DATA_FILEPATH = 'sample_data/*.txt'
TRANSCRIPT_ID_COL_IDX = 0
TRANSCRIPT_ABUNDANCE_COL_IDX = 8


def extract_sample_name(string):
    tokens = string.split('_')  # todo improve this
    return tokens[2] + '_' + tokens[3]


overall_set_collection = defaultdict(list)
sampled_transcripts_collection = defaultdict(dict)

unique_sample_names = []

for file_name in glob.glob(DATA_FILEPATH):
    # if file_name.endswith('tar.gz'):
    #     tar = tarfile.open(file_name)
    #     tar.extractall()
    #     tar.close()

    sample_name = extract_sample_name(file_name)
    unique_sample_names.append(sample_name)

    print 'starting: ' + sample_name

    # read and parse out transcript_ids and abundance values
    with open(file_name) as in_file:
        reader = csv.reader(in_file, delimiter='\t')
        next(reader, None)  # skip  the header row

        for line in [l for l in reader if l[1] != '-']:
            gene_id = line[TRANSCRIPT_ID_COL_IDX]
            abundance = line[TRANSCRIPT_ABUNDANCE_COL_IDX]
            sampled_transcripts_collection[gene_id][sample_name] = abundance

print 'genes count: ', len(sampled_transcripts_collection)
print 'sample_file count: ', len(unique_sample_names)

with open('test.csv', 'wb') as outfile:
    field_names = ['transcript_id'] + sorted(unique_sample_names)
    writer = csv.DictWriter(outfile, fieldnames=field_names)

    writer.writeheader()
    for transcript_id, t_dict in sorted(sampled_transcripts_collection.items()):
        row_dict = {'transcript_id': transcript_id}
        for sample_key in sorted(unique_sample_names):
            row_dict[sample_key] = t_dict.get(sample_key, 0)
        writer.writerow(row_dict)
