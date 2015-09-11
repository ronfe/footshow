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
    aC = (string.atof(updateA[0]) - matchTeam[0])
    dC = (string.atof(updateA[1]) - matchTeam[1])

    # update the league
    for each in leagueDict:
        originData = leagueDict[each]
        newData = [originData[0] + aC, originData[1] + dC]
        leagueDict[each] = newData

    # record
    g = open('teams/1516' + league + '.csv', 'w')
    for each in leagueDict:
        tempString = each + ',' + str(leagueDict[each][0]) + ',' + str(leagueDict[each][1]) + '\n'
        g.write(tempString)

    g.write(home + '\n')

    g.close()

data = probTable(0.05035242,-0.263849229111,-0.0701677856559,-0.25546449724,0.3220106)
a = match(data, 0, 2, [0.05035242,-0.263849229111,-0.0701677856559,-0.25546449724])
print a
# updateLeague('rus1', 'CSKA Moscow', a[0])
# updateLeague('por1', 'Sporting CP', a[1])
print 'done'