import os, sys, zipfile
src, dist, out = sys.argv[1], sys.argv[2], sys.argv[3]
prefix = "BOOT-INF/classes/web/"
new_files = {}
for root, _, files in os.walk(dist):
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, dist).replace(os.sep, "/")
        new_files[prefix + rel] = full
zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(out, "w")
for item in zin.infolist():
    if item.filename.startswith(prefix):
        continue  # drop all old web assets; replaced below
    zout.writestr(item, zin.read(item.filename), compress_type=item.compress_type)
for name, full in sorted(new_files.items()):
    with open(full, "rb") as fh:
        zout.writestr(name, fh.read(), compress_type=zipfile.ZIP_DEFLATED)
zout.close(); zin.close()
print("web files written:", len(new_files))
