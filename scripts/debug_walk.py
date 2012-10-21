import os

for (dirpath, dirnames, filenames) in os.walk(os.path.join("data", "pogs")):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        print path