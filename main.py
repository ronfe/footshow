__author__ = 'ronfe'
import string
from scipy.stats import poisson
from math import exp

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

def main(data, homeScore, awayScore, factor):
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

data = [0.11589818,0.18326767,0.14489891,0.07637533,0.03019273,0.00954864,0.00251652,0.00070422,0.06649792,0.10515194,0.08313742,0.04382123,0.01732343,0.00547864,0.00144388,0.00040405,0.01907697,0.03016607,0.02385053,0.01257147,0.00496976,0.00157172,0.00041422,0.00011592,0.00364854,0.00576938,0.00456151,0.00240434,0.00095049,0.00030060,0.00007922,0.00002217,0.00052335,0.00082756,0.00065430,0.00034488,0.00013634,0.00004312,0.00001136,0.00000318,0.00006006,0.00009496,0.00007508,0.00003958,0.00001565,0.00000495,0.00000130,0.00000036,0.00000574,0.00000908,0.00000718,0.00000378,0.00000150,0.00000047,0.00000012,0.00000003,0.00000051,0.00000080,0.00000063,0.00000033,0.00000013,0.00000004,0.00000001,0.00000000]

factor = [-0.9,-0.83,-0.37176429,-0.1319940]
# main(data,0,0,factor)