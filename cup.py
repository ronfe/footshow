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

homeTeam, homeAtt, homeDef = 'Manchester United',0.178586532052,-0.221596796491
awayTeam, awayAtt, awayDef = 'Ipswich Town',-0.145634333764,-0.824075867972

homeFactor = [0.2515865, 0.1959482]
homeScore, awayScore = 3,0

data = probTable(homeAtt,homeDef,awayAtt,awayDef,homeFactor[0])
a = match(data, homeScore, awayScore, [homeAtt,homeDef,awayAtt,awayDef])
print a
updateLeague('eng1', homeTeam, a[0])
updateLeague('eng2', awayTeam, a[1])
print 'done'