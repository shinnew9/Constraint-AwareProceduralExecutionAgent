This project uses the EPIC-KITCHENS dataset, specifically the annotation files provided by the EPIC-KITCHENS-100 release.


1. Data Source
EPIC-KITCHENS official website:
https://epic-kitchens.github.io/

EPIC-KITCHENS-100 annotation repository:
https://github.com/epic-kitchens/epic-kitchens-100-annotations



2. Required Files
Download the following annotation file:

EPIC_100_train.csv

This file contains action annotations in the form of verb-object pairs (e.g., "open drawer", "take cup") along with temporal information.



3. How to Download
1) Go to the repository:
   https://github.com/epic-kitchens/epic-kitchens-100-annotations

2) Download the following files directly from the repository:

   - EPIC_100_train.csv
   - EPIC_100_validation.csv



4. Where to Place the Data
After downloading, place the file in the following directory:

data/datasets/epic/

Final path should look like:

data/
 └── datasets/
      └── epic/
           └── EPIC_100_train.csv



5. How the Data is Used
This project does NOT use raw video files.

Instead, it uses the annotation CSV file to:

- Extract action sequences (verb-object pairs)
- Convert them into structured ActionGraph representations
- Perform constraint validation and scheduling

Example usage:

The adapter script converts annotation data into JSON format:

PYTHONPATH=src python src/capea/data/epic_adapter.py \
  --csv data/datasets/epic/EPIC_100_train.csv \
  --output data/examples/epic_window_0.json



6. Notes
- Only the annotation file is required for this project.
- No video download is needed.
- The dataset is large; ensure sufficient disk space.
- If the file path is incorrect, the scripts will fail to load data.