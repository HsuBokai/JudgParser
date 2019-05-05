#coding=utf-8
from __future__ import print_function
import csv
import re
import glob

data_folder = '/volume1/homes/admin/judg/'
CN_NUM = {
    u'0'  : 0, u'1'  : 1, u'2'  : 2, u'3'  : 3, u'4'  : 4, u'5'  : 5, u'6'  : 6, u'7'  : 7, u'8'  : 8, u'9'  : 9,
    u'〇' : 0, u'一' : 1, u'二' : 2, u'三' : 3, u'四' : 4, u'五' : 5, u'六' : 6, u'七' : 7, u'八' : 8, u'九' : 9,
    u'零' : 0, u'壹' : 1, u'貳' : 2, u'叄' : 3, u'肆' : 4, u'伍' : 5, u'陸' : 6, u'柒' : 7, u'捌' : 8, u'玖' : 9,
    u'貮' : 2, u'兩' : 2, u'參' : 3,
}
CN_UNIT = {
    u'十' : 10, u'拾' : 10,
    u'百' : 100, u'佰' : 100,
    u'千' : 1000, u'仟' : 1000,
    u'萬' : 10000, u'萬' : 10000,
    u'億' : 100000000, u'億' : 100000000,
    u'兆' : 1000000000000,
}

def test_parse_cn_number():
    test_dig = [
        u'八',
        u'十一',
        u'一百二十三',
        u'一千二百零三',
        u'一萬一千一百零一',
        u'十萬零三千六百零九',
        u'一百二十三萬四千五百六十七',
        u'一千一百二十三萬四千五百六十七',
        u'一億一千一百二十三萬四千五百六十七',
        u'一百零二億五千零一萬零一千零三十八',
    ]
    for t in test_dig:
        print(t)
        print(parse_cn_number(t))

def parse_cn_number(cn):
    unit = 0   # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig, None)
            if unit is None:
                return 0
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig, None)
            if dig is None:
                return 0
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val

def parse_punish_month(cn):
    year, month = 0, 0
    if cn.find(u'年') is not -1:
        year = parse_cn_number(cn.split(u'年')[0])
        if cn.find(u'月') is not -1:
            month = parse_cn_number(cn.split(u'年')[1].split(u'月')[0])
    else:
        if cn.find(u'月') is not -1:
            month = parse_cn_number(cn.split(u'月')[0])
    return year * 12 + month

def parse_adjudged_on(s):
    year = 1911 + int(s[:-4])
    return str(year) + '-' + s[-4:-2] + '-' + s[-2:]

def parse_csv(f):
    re_minus_punishment = re.compile(u'減為有期徒刑(.+?)，')
    re_punishment = re.compile(u'徒刑(.+?)，')
    text = []
    with open(f, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            row_list = [entry.decode("utf8") for entry in row]
            text.append(row_list)
    maintext = ''.join(text[4]).split(u'事  實')[0]
    if re_minus_punishment.search(maintext) is not None:
        result = re_minus_punishment.findall(maintext)
    else:
        result = re_punishment.findall(maintext)
    punish_month = map(parse_punish_month, result)
    if punish_month:
        #print f
        print('(\'%s\', %d), ' % (parse_adjudged_on(text[1][1]), max(punish_month)), end='')

def main():
    csv.field_size_limit(8388608)
    files = glob.glob(data_folder + '*/*.csv')
    for f in files:
        parse_csv(f)

if __name__ == "__main__":
    main()
