import csv
import glob
import gzip
from collections import defaultdict

import logging
import progressbar

progressbar.streams.wrap_stderr()
logging.basicConfig(level=logging.INFO)

DATA_FILEPATH = 'sample_data/*.txt.gz'
TRANSCRIPT_ID_COL_IDX = 0
TRANSCRIPT_ABUNDANCE_COL_IDX = 8

sampled_transcripts_collection = defaultdict(dict)
unique_sample_names = set()


def extract_sample_name(string):
    tokens = string.split('_')  # todo improve this
    return tokens[2] + '_' + tokens[3]


sample_set_files = glob.glob(DATA_FILEPATH)

logging.info('Processing files..')
with progressbar.ProgressBar(max_value=len(sample_set_files)) as bar:
    for i in range(0, len(sample_set_files)):
        file_name = sample_set_files[i]

        sample_name = extract_sample_name(file_name)
        unique_sample_names.add(sample_name)

        with gzip.open(file_name, 'rb') as in_file:
            reader = csv.reader(in_file, delimiter='\t')
            next(reader, None)  # skip the header row

            data = list(reader)

            current_transcript_counter = 0
            for line in [l for l in data if l[1] != '-']:
                current_transcript_counter += 1
                gene_id = line[TRANSCRIPT_ID_COL_IDX]
                abundance = line[TRANSCRIPT_ABUNDANCE_COL_IDX]
                sampled_transcripts_collection[gene_id][sample_name] = abundance

            logging.info('   %s: %i/%i', sample_name, current_transcript_counter, len(data))
        bar.update(i)

logging.info('# unique transcript_ids: %i', len(sampled_transcripts_collection))
logging.info('writing the results..')

with open('out.csv', 'wb') as outfile:
    field_names = ['transcript_id'] + sorted(unique_sample_names)
    writer = csv.DictWriter(outfile, fieldnames=field_names)

    writer.writeheader()
    for transcript_id, t_dict in sorted(sampled_transcripts_collection.items()):
        row_dict = {'transcript_id': transcript_id}
        for sample_key in sorted(unique_sample_names):
            row_dict[sample_key] = t_dict.get(sample_key, 0)
        writer.writerow(row_dict)
