__author__ = 'ronfe'

import string
from scipy.stats import poisson
from math import exp


def parameters(filePath):
    # read match files
    f = open(filePath).readlines()

    # pick teams
    teams = []
    games = []
    for each in f:
        tempGroup = each.strip().split(',')
        teams.append(tempGroup[0])
        teams.append(tempGroup[1])
        games.append(tempGroup)

    teams = list(set(teams))
    teams.sort()

    n = len(teams)
    g = len(games)

    # construct matrix
    Y = []
    Home = []
    for each in range(0, 2*g):
        Y.append([0])
        Home.append(0)

    # fill data
    for i in range(0, g):
        match = games[i]
        homeScore = match[2]
        awayScore = match[3]

        Y[2*i] = homeScore
        Y[(2*i+1)] = awayScore

    X = [[0 for _ in xrange(2*n)] for _ in xrange(2*g)]

    for i in range(0, g):
        homeTeam = games[i][0]
        awayTeam = games[i][1]

        M = teams.index(homeTeam)
        N = teams.index(awayTeam)

        X[2*i][M] = 1
        X[2*i][N+n] = -1
        X[2*i+1][N] = 1
        X[2*i+1][M+n] = -1

        Home[2*i] = 1





