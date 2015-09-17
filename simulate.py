__author__ = 'ronfe'
import os, string
from predict import predict

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

league = 'eng1'
homeFactor = 0.2515865

# generate match list
f = open('./teams/1516' + league + '.csv').readlines()

clubs = []
atts = []
defs = []
for each in f:
    tempGroup = each.strip().split(',')
    if len(tempGroup) == 3:
        clubs.append(tempGroup[0])
        atts.append(tempGroup[1])
        defs.append(tempGroup[2])

matches = []

standing = {}
for i in clubs:
    standing[i] = [0,0,0,0]
    for j in clubs:
        if i != j:
            matches.append('eng1,' + i + ',' + j)



# calc match results and record
results = []

for each in matches:
    tM = each.strip()
    tempElem = predict(tM, False, 0)
    results.append(tempElem)


g = open('./simulation/' + league + '.csv', 'w')
for each in results:
    g.write(each + '\n')

# calc standing


for each in results:
    tempMatch = each.split(',')
    home = tempMatch[1]
    away = tempMatch[2]
    homeScore = string.atoi(tempMatch[3])
    awayScore = string.atoi(tempMatch[4])

    if homeScore > awayScore:
        standing[home][0] += 3

    elif homeScore == awayScore:
        standing[home][0] += 1
        standing[away][0] += 1
    else:
        standing[away][0] += 3

    standing[home][1] += (homeScore - awayScore)
    standing[away][1] += (awayScore - homeScore)
    standing[home][2] += homeScore
    standing[away][2] += awayScore
    standing[home][3] += awayScore
    standing[away][3] += homeScore

print standing['Chelsea']

h = open('./simulation/table.csv', 'w')
for k, v in standing:
    h.write(k + ',')

g.close()