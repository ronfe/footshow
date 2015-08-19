__author__ = 'ronfe'
import string
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def mean(data):
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/float(n)

def _ss(data):
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

def showTable(league):
    f = open('teams/1516'+ league + '.csv').readlines()
    teams = {}
    coefficients = []
    for each in f:
        if '$home' not in each:
            team, attack, defend = each.strip().split(',')
            teams[team] = [string.atof(attack), string.atof(defend)]
            coefficients.append(string.atof(attack))
            coefficients.append(string.atof(defend))

    kmean = mean(coefficients)
    std = pstdev(coefficients)

    for each in teams:
        revisedAtt = ((teams[each][0] - kmean) / std)
        revisedDef = ((teams[each][1] - kmean) / std)
        print each + ',' + str(revisedAtt) + ',' + str(revisedDef) + ',' + str(round(revisedAtt + revisedDef, 2))

    print ''
    print 'done'

showTable('eng2')