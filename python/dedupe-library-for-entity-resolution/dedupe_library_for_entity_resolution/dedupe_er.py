import os
import csv
import re

import dedupe
from unidecode import unidecode

from dedupe_library_for_entity_resolution import hack_convenience


class DedupeER:

    def __init__(self, fields: []) -> None:
        self.fields = fields

    @staticmethod
    def pre_process(column):
        #
        column = unidecode(column)
        column = re.sub('  +', ' ', column)
        column = re.sub('\n', ' ', column)
        column = column.strip().strip('"').strip("'").lower().strip()
        #

        if not column:
            column = None
        return column

    #

    @staticmethod
    def read_csv(filename):
        #
        data_d = {}
        with open(filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = [(k, DedupeER.pre_process(v)) for (k, v) in row.items()]
                row_id = int(row['Id'])
                data_d[row_id] = dict(clean_row)

        return data_d

    def run(self, working_path):
        input_file = f'{working_path}/input.csv'
        output_file = f'{working_path}/output.csv'
        settings_file = f'{working_path}/learned_settings'
        training_file = f'{working_path}/training.json'

        print('importing data ...')
        data_d = DedupeER.read_csv(input_file)

        if os.path.exists(settings_file):
            print('reading from', settings_file)
            with open(settings_file, 'rb') as f:
                deduper = dedupe.StaticDedupe(f)
        else:

            dd_fields = self.fields
            deduper = dedupe.Dedupe(dd_fields)
            if os.path.exists(training_file):
                print('reading labeled examples from ', training_file)
                with open(training_file, 'rb') as f:
                    deduper.prepare_training(data_d, f)
            else:
                deduper.prepare_training(data_d)
            #

            print('starting active labeling...')

            hack_convenience.console_label(deduper)

            # dedupe.console_label(deduper)
            #

            deduper.train()
            #

            with open(training_file, 'w') as tf:
                deduper.write_training(tf)
            #

            with open(settings_file, 'wb') as sf:
                deduper.write_settings(sf)
        #

        print('clustering...')
        clustered_dupes = deduper.partition(data_d, 0.5)

        print('# duplicate sets', len(clustered_dupes))
        #

        cluster_membership = {}
        for cluster_id, (records, scores) in enumerate(clustered_dupes):
            for record_id, score in zip(records, scores):
                cluster_membership[record_id] = {
                    "Cluster ID": cluster_id,
                    "confidence_score": score
                }

        with open(output_file, 'w') as f_output, open(input_file) as f_input:

            reader = csv.DictReader(f_input)
            fieldnames = ['Cluster ID', 'confidence_score'] + reader.fieldnames

            writer = csv.DictWriter(f_output, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                row_id = int(row['Id'])
                row.update(cluster_membership[row_id])
                writer.writerow(row)
