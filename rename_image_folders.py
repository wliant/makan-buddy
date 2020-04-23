import os

errors = []
for f in os.listdir("data/images"):
    p2 = os.path.join("data/images", f)
    for f2 in os.listdir(p2):
        path = os.path.join(p2, f2)
        if os.path.isdir(path):
            splits = f2.split("_")
            if len(splits) > 2:
                try:
                    renamed = os.path.join(p2, "{}_{}".format(splits[0], splits[1]))
                    os.rename(path, renamed)
                    print("renamed: {}".format(renamed))
                except Exception as e:
                    errors.append({"message": str(e), "path": path})
            else:
                print("not renamed: {}".format(path))

for i in errors:
    print(i)
