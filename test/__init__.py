import zipfile

tmp_file = f"/home/badcw/Desktop/test.zip"
total_name = []
count = 0
with zipfile.ZipFile(tmp_file, "r") as zip_file:
    name_list = zip_file.namelist()
    for item in name_list:
        if "/problem.json" in item:
            total_name.append(item[:-13])
            count += 1

    for i in total_name:
        with zip_file.open(f"{i}/problem.json") as f:
            print(f"{i}/testcase/")