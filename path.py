import sys

def getpath():
    if sys.platform.startswith('linux'):
        path = "/opt/application/webtop/bowl_judgment"
    else:
        path = '.'
        
    return path
