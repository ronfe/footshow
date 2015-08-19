__author__ = 'ronfe'
from main import probTable, match
import string

def updateLeague(league, team, updateA):
    f = open('teams/1516' + league + '.csv').readlines()
    # convert to dict
    leagueDict = {}
    home = ''
    for each in f:
        if '$home' not in each:
            tempTeam, attack, defence = each.strip().split(',')
            attack = string.atof(attack)
            defence = string.atof(defence)
            leagueDict[tempTeam] = [attack, defence]
        else:
            home = each
    # calc the rate
    matchTeam = leagueDict[team]
    aC = (string.atof(updateA[0]) - matchTeam[0]) / abs(matchTeam[0])
    dC = (string.atof(updateA[1]) - matchTeam[1]) / abs(matchTeam[1])
    attackRate = abs(aC * matchTeam[0]) * (aC / abs(aC)) + matchTeam[0]
    defendRate = abs(dC * matchTeam[1]) * (dC / abs(dC)) + matchTeam[1]

    # update the league
    for each in leagueDict:
        originData = leagueDict[each]
        newData = [abs(aC * originData[0]) * (aC / abs(aC)) + originData[0], abs(dC * originData[1]) * (dC / abs(dC)) + originData[1]]
        leagueDict[each] = newData

    # record
    g = open('teams/1516' + league + '.csv', 'w')
    for each in leagueDict:
        tempString = each + ',' + str(leagueDict[each][0]) + ',' + str(leagueDict[each][1]) + '\n'
        g.write(tempString)

    g.write(home + '\n')

    g.close()

data = probTable(0.9257872,0.726743231386,0.887162603291,0.57925995,0.3306335)
a = match(data, 2, 1, [0.9257872,0.726743231386,0.887162603291,0.57925995])
updateLeague('por1', 'Sporting CP', a[0])
updateLeague('rus1', 'CSKA Moscow', a[1])
print 'done'