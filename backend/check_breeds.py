import sys
sys.path.insert(0, r'E:\dog_doctor\dog-doctor\backend')
from breeds_data import BREEDS_DATA

print('Total breeds:', len(BREEDS_DATA))
print('name_en format samples:')
for b in BREEDS_DATA[:10]:
    print(f'  breed_id={b["breed_id"]}, name_en="{b["name_en"]}"')
print()

# Check how many have spaces in name_en
with_space = [b for b in BREEDS_DATA if ' ' in b['name_en']]
print(f'Breeds with spaces in name_en: {len(with_space)}')
if with_space:
    for b in with_space[:10]:
        print(f'  {b["name_en"]}')

# Check if name_en matches breed_mapping format
print()
print('Checking match with breed_mapping...')
sys.path.insert(0, r'E:\dog_doctor\dog-doctor\backend')
from ml.breed_mapping import BREED_MAP
mapping_names = set(b["name_en"].lower() for b in BREED_MAP)

mismatch = []
for b in BREEDS_DATA:
    if b["name_en"].lower().replace(' ', '_') not in mapping_names:
        mismatch.append(b["name_en"])
print(f'Breeds whose name_en (lower, space->underscore) NOT in breed_mapping: {len(mismatch)}')
if mismatch:
    for name in mismatch[:10]:
        print(f'  "{name}"')
