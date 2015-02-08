import fnmatch
import os
import re
os.system("wget -P blog -mpck -np -nH -E 127.0.0.1:2368")

static_path = "blog/"
versioned_assets = []
for root, dirs, filenames in os.walk(static_path):
    for filename in filenames:
        if "@v=" in filename:
            versioned_assets.append(filename)

# Clean up copied files
excludes = ['*.jpeg', '*.jpg', '*.gif', '*.png']
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

for root, dirs, filenames in os.walk(static_path):
    filenames = [f for f in filenames if not re.match(excludes, f)]
    for filename in filenames:
        data = None
        with open(os.path.join(root, filename), 'rb') as open_file:
            data = open_file.read()
        if "ghostHunter-init.js" in filename:
            data = data.replace('rss: "/rss"', 'rss: "/rss/index.xml"')
        for asset_file in versioned_assets:
            new_filename = asset_file.split("@v=", 1)[0]
            data = data.replace(asset_file, new_filename)
        data = data.replace("/index.html", "")
        data = data.replace("http://localhost:2368", "https://www.atindriyaghosh.com")
        with open(os.path.join(root, filename), 'wb') as open_file:
            open_file.write(data)
        if filename in versioned_assets:
            os.rename(os.path.join(root, filename), os.path.join(
                root, filename.split("@v=", 1)[0]))
        if root.endswith("/rss"):
            os.rename(os.path.join(root, filename), os.path.join(
                root, os.path.splitext(filename)[0] + ".xml"))
