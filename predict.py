__author__ = 'ronfe'
import string
from main import probTable

def predict(info, isNeutral, rangqiu):
    # homeTeam / awayTeam should be 'leagueName, homeTeam, awayTeam'
    league, home, away = info.split(',')

    # Read data
    f = open('teams/1516'+league + '.csv').readlines()
    for each in f:
        if home in each:
            homeName, homeAtt, homeDef = each.strip().split(',')
        elif away in each:
            awayName, awayAtt, awayDef = each.strip().split(',')
        elif '$home' in each:
            homeFactor = each.strip().split('=')[1]

    homeAtt = string.atof(homeAtt)
    homeDef = string.atof(homeDef)
    awayAtt = string.atof(awayAtt)
    awayDef = string.atof(awayDef)
    if isNeutral:
        homeFactor = 0
    else:
        homeFactor = string.atof(homeFactor)

    # get probtable
    data = probTable(homeAtt, homeDef, awayAtt, awayDef, homeFactor)

    # calc prediction
    nestedData = []
    pointer = 8
    while pointer <= 64:
        nestedData.append(data[pointer - 8:pointer])
        pointer += 8
    maxIndex = data.index(max(data))
    idealHomeScore = maxIndex / 8
    idealAwayScore = maxIndex % 8
    winProb = 0
    drawProb = 0
    loseProb = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if (i + rangqiu < j):
                loseProb += nestedData[i][j]
            elif (i + rangqiu == j):
                drawProb += nestedData[i][j]
            elif (i + rangqiu > j):
                winProb += nestedData[i][j]


    print 'Prediction of ' + home + ' vs ' + away
    if (rangqiu != 0):
        print 'With Rangqiu of ' + str(rangqiu)
    print 'Win: ' + str(round(winProb*100, 2)) + '\t' + 'Draw: ' + str(round(drawProb*100, 2)) + '\t' + 'Lose: ' + str(round(loseProb*100, 2))
    print 'Recommended Score: ' + str(idealHomeScore) + ' - ' + str(idealAwayScore)

g = open('predict.csv').readlines()
k = open('match.csv', 'w')
for m in g:
    tM = m.strip()
    predict(tM, False)
    k.write(m)

g = open('predict.csv', 'w')
g.write('')
g.close()
k.close()

# predict('eng2,Hull City,Fulham', False, -1)

print 'done'