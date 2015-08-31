__author__ = 'ronfe'
import string
import os
from scipy.stats import norm

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
        revisedAtt = norm.cdf(teams[each][0], kmean, std) * 100
        revisedDef = norm.cdf(teams[each][1], kmean, std) * 100
        print each + ',' + str(int(revisedAtt)) + ',' + str(int(revisedDef)) + ',' + str(round(revisedAtt + revisedDef, 2))

    print ''
    print 'done'

showTable('esp1')
showTable('esp2')
showTable('eng1')
showTable('eng2')
showTable('ger1')
showTable('ger2')
showTable('ita1')
showTable('fra1')
showTable('por1')
showTable('rus1')