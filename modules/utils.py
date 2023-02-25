import glob

def recent_file(path,extension,location):
    files = glob.glob(path + extension)
    max_file=sorted(files,key=os.path.getctime)[-location]
    return max_file