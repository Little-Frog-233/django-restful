from myDjangoRestful.model.mysql import *

def getAllChart():
    return Chart.objects.all()

if __name__ == '__main__':
    print(BASE_DIR)