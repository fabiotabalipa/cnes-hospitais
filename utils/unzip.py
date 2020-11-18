from zipfile import ZipFile


def unzip(file, target_dir):
    with ZipFile(file, "r") as zipObj:
        zipObj.extractall(target_dir)
