__author__ = 'ronfe'
import string
from scipy.stats import poisson
from math import exp

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def probTable(homeAtt, homeDef, awayAtt, awayDef, homeFactor):
    lambdaA = exp(homeAtt - awayDef + homeFactor)
    lambdaB = exp(awayAtt - homeDef)

    A = []
    B = []

    remA = 0
    remB = 0

    for i in range(0, 7):
        tempPois = poisson.cdf(i, lambdaA)
        A.append(tempPois - remA)
        remA = tempPois
        tempPois = poisson.cdf(i, lambdaB)
        B.append(tempPois - remB)
        remB = tempPois

    A.append(1 - remA)
    B.append(1 - remB)

    result = []
    for i in range(0, 8):
        for j in range(0, 8):
            result.append(A[i] * B[j])

    return result

def match(data, homeScore, awayScore, factor):
    # factor is a list of [homeAttack, homeDefence, awayAttack, awayDefence]
    nestedData = []
    pointer = 8
    while pointer <= 64:
        nestedData.append(data[pointer - 8:pointer])
        pointer += 8
    maxIndex = data.index(max(data))
    idealHomeScore = maxIndex / 8
    idealAwayScore = maxIndex % 8
    print 'Guessing ' + str(idealHomeScore) + ' - ' + str(idealAwayScore) + ' ; Possibility: ' + str(round(max(data), 4))
    print 'Real ' + str(homeScore) + ' - ' + str(awayScore) + ' ; Possibility: ' + str(round(nestedData[homeScore][awayScore], 4))

    # Calc home factor
    tempProb = 0
    deltaAttack = 0
    deltaDefence = 0
    if homeScore > idealHomeScore:
        tempProb = nestedData[homeScore][idealAwayScore]
        deltaAttack = abs(tempProb - max(data))
    elif homeScore == idealHomeScore:
        tempProb = nestedData[idealHomeScore][idealAwayScore]
    elif homeScore < idealHomeScore:
        tempProb = nestedData[homeScore][idealAwayScore]
        deltaAttack = -abs(tempProb - max(data))

    if awayScore < idealAwayScore:
        deltaDefence = abs(tempProb - nestedData[homeScore][awayScore])
    elif awayScore == idealAwayScore:
        deltaDefence = 0
    elif awayScore > idealAwayScore:
        deltaDefence = -abs(tempProb - nestedData[homeScore][awayScore])

    print ''
    print 'For home team: '
    print 'The attack should add ' + str(deltaAttack) + ' to be ' + str(factor[0] + deltaAttack)
    print 'The defence should add ' + str(deltaDefence) + ' to be ' + str(factor[1] + deltaDefence)
    homeF = [str(factor[0] + deltaAttack), str(factor[1] + deltaDefence)]

    # calc away factor
    tempProb = 0
    deltaAttack = 0
    deltaDefence = 0
    if awayScore > idealAwayScore:
        tempProb = nestedData[idealHomeScore][awayScore]
        deltaAttack = abs(tempProb - max(data))
    elif awayScore == idealAwayScore:
        tempProb = nestedData[idealHomeScore][idealAwayScore]
    elif awayScore < idealAwayScore:
        tempProb = nestedData[idealHomeScore][awayScore]
        deltaAttack = -abs(tempProb - max(data))

    if homeScore < idealHomeScore:
        deltaDefence = abs(tempProb - nestedData[homeScore][awayScore])
    elif homeScore == idealHomeScore:
        deltaDefence = 0
    elif homeScore > idealHomeScore:
        deltaDefence = -abs(tempProb - nestedData[homeScore][awayScore])

    print ''
    print 'For away team: '
    print 'The attack should add ' + str(deltaAttack) + ' to be ' + str(factor[2] + deltaAttack)
    print 'The defence should add ' + str(deltaDefence) + ' to be ' + str(factor[3] + deltaDefence)
    awayF = [str(factor[2] + deltaAttack), str(factor[3] + deltaDefence)]

    return [homeF, awayF]

def initMatchDay():
    matches = open('match.csv').readlines()
    for each in matches:
        # STEP 0: data preparation
        each = each.strip()
        league, home, away, homeScore, awayScore = each.split(',')
        homeScore = string.atoi(homeScore)
        awayScore = string.atoi(awayScore)

        # fetch home / away team info
        fileName = './teams/1516' + league + '.csv'
        teams = open(fileName).read()
        homeT = teams[teams.index(home):].split('\n')[0]
        awayT = teams[teams.index(away):].split('\n')[0]

        home, homeAtt, homeDef = homeT.split(',')
        homeAtt = string.atof(homeAtt)
        homeDef = string.atof(homeDef)

        away, awayAtt, awayDef = awayT.split(',')
        awayAtt = string.atof(awayAtt)
        awayDef = string.atof(awayDef)

        # fetch homefactor
        homeFactor = string.atof(teams.split('\n')[-1].split('=')[1])

        # STEP 1: record match information
        matchRecord = home + ',' + away + ',' + str(homeScore) + ',' + str(awayScore) + '\n'
        g = open('./1516results/' + league + '.csv', 'a')
        g.write(matchRecord)
        g.close()

        # STEP 2: get the probtable
        prob = probTable(homeAtt, homeDef, awayAtt, awayDef, homeFactor)
        factor = [homeAtt, homeDef, awayAtt, awayDef]

        # STEP 3: update data and record
        changes = match(prob, homeScore, awayScore, factor)
        homeChange = home + ','.join(changes[0])
        awayChange = away + ','.join(changes[1])

        teamList = open(fileName).readlines()
        newTeamList = []
        for eachOne in teamList:
            if (home not in eachOne) and (away not in eachOne):
                newTeamList.append(eachOne)

        newTeamList.append(homeChange)
        newTeamList.append(awayChange)

        g = open(fileName, 'w')
        for eachTwo in newTeamList:
            g.write(eachTwo + '\n')

        g.close()

    print 'done'

initMatchDay()
