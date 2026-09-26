import os
import glob
import re

models_dir = 'trace/backend/app/models'
for filepath in glob.glob(os.path.join(models_dir, '*.py')):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We want to replace Column(SAEnum(MyEnum), ...) with Column(SAEnum(MyEnum, values_callable=lambda obj: [e.value for e in obj]), ...)
    # Pattern: SAEnum(EnumName)
    # Using regex to find SAEnum(Word) and replace it
    new_content = re.sub(r'SAEnum\(([A-Za-z0-9_]+)\)', r'SAEnum(\1, values_callable=lambda obj: [e.value for e in obj])', content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Patched {filepath}")
