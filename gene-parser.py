import csv
import glob
from collections import defaultdict
import sys
import tarfile

DATA_FILEPATH='data/GSM3515624_CF10_L004_gene_abund.out.txt'
# DATA_FILEPATH = 'data/*.csv'
TRANSCRIPT_ID_COL_IDX = 0
TRANSCRIPT_ABUNDANCE_COL_IDX = 8


def get_sample_name(string):
    tokens = string.split('_')
    return tokens[1] + '_' + tokens[2]


def parse_transcript_rows(raw_rows):
    result = []
    for row in raw_rows:
        if row[1] != '-':
            result.append([row[TRANSCRIPT_ID_COL_IDX], row[TRANSCRIPT_ABUNDANCE_COL_IDX]])
    return sorted(result)


sampled_transcript_ids = []
unique_transcript_ids = set()
unique_samples = set()

for filename in glob.glob(DATA_FILEPATH):
    sample_name = get_sample_name(filename)
    unique_samples.add(sample_name)

    # read and parse out transcript_ids and abundance values
    with open(filename) as in_file:
        reader = csv.reader(in_file, delimiter='\t')
        next(reader, None)  # skip  the headers

        result = []
        for row1 in reader:
            transcript_id = row1[TRANSCRIPT_ID_COL_IDX]
            unique_transcript_ids.add(transcript_id)

            if row[1] != '-':
                result.append((transcript_id, u))

        for row in sorted(result):
            transcript_id, abundance = row
            data = (transcript_id, sample_name, abundance)
            sampled_transcript_ids.append(data)

print 'unique transcript ids: ', len(unique_transcript_ids)
print 'unique samples: ', len(unique_samples)
print 'total sampled transcripts: ', len(sampled_transcript_ids)

for transcript_id in sorted(unique_transcript_ids):
    transcript_dict = defaultdict(dict)
    for sample_name in sorted(unique_samples):
        transcript_dict[transcript_id][sample_name] = None
        for match in [t for t in sampled_transcript_ids if t[:2] == (transcript_id, sample_name)]:
            transcript_dict[transcript_id][sample_name] = match[2]

print(sorted(transcript_dict.items()))

