import unittest
from pathlib import Path

import pandas as pd

from dedupe_library_for_entity_resolution import dedupe_er


class DedupeERTests(unittest.TestCase):

    def test_entity_resolution(self):
        df = pd.read_csv(
            'https://raw.githubusercontent.com/dedupeio/dedupe-examples/master/csv_example/csv_example_messy_input.csv'
        )

        fields = [
            {'field': 'Site name', 'type': 'String'},
            {'field': 'Address', 'type': 'String'},
            {'field': 'Zip', 'type': 'Exact', 'has missing': True},
            {'field': 'Phone', 'type': 'String', 'has missing': True},
        ]

        Path("build").mkdir(parents=True, exist_ok=True)

        df.to_csv("build/input.csv", index=False)

        der = dedupe_er.DedupeER(fields=fields)

        der.run(working_path="build")

        self.assertIsNotNone(dedupe_er)


if __name__ == "__main__":
    unittest.main()
