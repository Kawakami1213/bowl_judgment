import sys

def getpath():
    if sys.platform.startswith('linux'):
        path = "/opt/application/webtop/bowl_judgment"
        uploadfolder = "/opt/application/webtop/bowl_judgment/uploads"
    else:
        path = '.'
        uploadfolder = 'uploads'

    return path, uploadfolder
