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

homeTeam, homeAtt, homeDef = 'Monaco',0.501548040131,0.413951616658
awayTeam, awayAtt, awayDef = 'Tottenham Hotspur',0.220248413429,-0.413833298416

homeFactor = [0.2639907]
homeScore, awayScore = 1,1

data = probTable(homeAtt,homeDef,awayAtt,awayDef,homeFactor[0])
a = match(data, homeScore, awayScore, [homeAtt,homeDef,awayAtt,awayDef])
print a
updateLeague('fra1', homeTeam, a[0])
updateLeague('eng1', awayTeam, a[1])
print 'done'