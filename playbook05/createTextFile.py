from os import listdir
from os.path import isfile, join
import pandas as pd
import re

FILEPATH = "./accumilated.txt"
TEXTFILE = "IMDAICOP.txt"


def createSet(sheetDf):
    flag = 0
    categoryPattern = re.compile(r'.*\(\w.*\)')
    websitePattern = re.compile(r'([\w]+.*)(\.)([a-z]{2,})')
    sheetTop = sheetDf.columns.values
    if re.match(categoryPattern, sheetTop[0]):
        if 'Scam Sites' in sheetTop[0]:
            flag = 1
        else:
            flag = 0
    for index, row in sheetDf.iterrows():
        if re.match(categoryPattern, str(row[0])):
            if 'Scam Sites' in row[0]:
                flag = 1
            else:
                flag = 0
        if re.match(websitePattern, str(row[1])):
            if flag == 0:
                yield('".'+row[1]+'" := "rpz_mda"')
            else:
                yield('".'+row[1]+'" := "rpz_fraud"')


def writeTotextFile(urlList):
    with open(TEXTFILE, 'w+') as f:
        [f.write("%s\n" % item) for item in urlList]


def main():
    urlList = []
    sheets = pd.read_excel(FILEPATH, sheet_name=None)
    [urlList.extend(createSet(sheetData)) for sheetData in sheets.values()]
    writeTotextFile(urlList)


if __name__ == "__main__":
    main()

