#!/usr/bin/env python

import json
import sys
from collections import defaultdict

FILENAME = sys.argv[1]
USERID = 3

###########################################################################

# Dectorator to speed up reading from files
def memoize(function):
  memo = {}
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper


###########################################################################

dump = json.load(open(FILENAME, 'r'))

###########################################################################

@memoize
def get(database, field, content):
    result = []
    for entry in dump[database]['entries']:
        if entry[field] == content:
            result.append(entry)

    return result

###########################################################################

# direction: 'in' or 'out'
def getDelegations(direction):
    if (direction == 'in'):
        delegeation_me = 'trustee_id'
        delegeation_them = 'truster_id'
    else:
        delegeation_me = 'truster_id'
        delegeation_them = 'trustee_id'

    area_delegations = defaultdict(set)
    unit_delegations = set()

    for delegation in dump['area_delegation']['entries']:
        if delegation[delegeation_me] == USERID:
            if (delegation['scope'] == 'unit'):
                unit_delegations.add(delegation[delegeation_them])
            else:
                area_delegations[delegation['area_id']].add(delegation[delegeation_them])

    return (area_delegations, unit_delegations)

###########################################################################

# eingehende Delegationen
(area_delegation, unit_delegation) = getDelegations('in')

if (len(unit_delegation) > 0 or len(area_delegation) > 0):
    print "Eingehende Delegationen:"

if len(unit_delegation) > 0:
    print "- Globaldelegationen: " + str(len(unit_delegation))

for area in area_delegation:
    print "- Thema \"" + get('area', 'id', area)[0]['name'] + "\": " + str(len(area_delegation[area]))

# ausgehende Delegationen
(area_delegation, unit_delegation) = getDelegations('out')

if (len(unit_delegation) > 0 or len(area_delegation) > 0):
    print "Ausgehende Delegationen:"
for p in unit_delegation:
    print "- Globaldelegation an " + get('member', 'id', p)[0]['name']
else:
    for area in area_delegation:
        for p in area_delegation[area]:
            print "- Thema \"" + get('area', 'id', area)[0]['name'] + "\" an " + get('member', 'id', p)[0]['name']

###########################################################################

#print
#for issue in dump['issue']['entries']:
#    if issue['closed'] != None:
#        print("Thema " + str(issue['id']))
#        #print(issue['area_id'], issue['id'])
#        initiatives = get('initiative', 'issue_id', issue['id'])
#        for initiative in initiatives:
#            if initiative['rank'] != None:
#                print "-", initiative['name'], initiative['rank']
#            else:
#                print "-", initiative['name'], "--"
#        print
#        #print(len(initiatives))
        