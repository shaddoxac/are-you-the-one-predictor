lastIndex = 10 ## will go through at most the first {lastIndex} days

class Odds:
    def __init__(self):
        self.lightOdds = []

    def add(self, matchName, numerator, divisor):
        self.lightOdds.append((matchName, numerator, divisor))

    def overallOdds(self, remainingPossible):
        return 1.0 / remainingPossible

    def intDivide(self, a, b):
        return (a + 0.0) / b

    def calculateCurrentOdds(self, possibleMatches):
        numPossible = len(possibleMatches)
        bestMatchFound = {} # dict of [matchName -> (best found odds per person, divisor used)]

        for matchName in possibleMatches:
            bestMatchFound[matchName] = (1, numPossible) # start with naive, update later if more accurate odds are found

        for (matchName, numerator, divisor) in self.lightOdds:
            if divisor > 0:
                foundOdds = self.intDivide(numerator, divisor)
                existingOdds = self.intDivide(bestMatchFound[matchName][0], bestMatchFound[matchName][1])
                if (foundOdds > existingOdds): # use best found odds
                    print(f'{foundOdds} was greater than {existingOdds}')
                    bestMatchFound[matchName] = (numerator, divisor)

        # todo, move to new function
        totalDivisorSumFromLights = 1 # get divisor to force everything to same scale
        for matchName in bestMatchFound:
            totalDivisorSumFromLights *= bestMatchFound[matchName][1]

        adjustedNumerators = {} # put everything in relation to the same divisor
        for matchName in possibleMatches:
            (currentNumerator, currentDivisor) = bestMatchFound[matchName]
            adjustedNumerators[matchName] = self.intDivide(currentNumerator *  totalDivisorSumFromLights, currentDivisor)

        sumOfNumerators = 0
        for matchName in possibleMatches:
            sumOfNumerators += adjustedNumerators[matchName]

        returnValues = {} # dict of match name -> percentage chance
        for matchName in possibleMatches:
            print(f'{matchName} - {adjustedNumerators[matchName]} - {sumOfNumerators}')
            returnValues[matchName] = adjustedNumerators[matchName] / sumOfNumerators

        return returnValues

class Possibilities:

    def __init__(self, males, females):
        self.possibilities = []
        self.males = males
        self.females = females
        self.numMales = len(males)
        self.numFemales = len(females)

        maleIndexes   = [-1] * self.numMales
        femaleIndexes = [-1] * self.numFemales
        self.initialCombinations(maleIndexes, femaleIndexes)

    def initialCombinations(self, maleIndexes, femaleIndexes):
        numMatched = 0
        for maleIndex in range(0, self.numMales):
            if maleIndexes[maleIndex] == -1: # if this male does not already have a match..
                numMatched += 1

                for femaleIndex in range(0, self.numFemales):
                    if femaleIndexes[femaleIndex] == -1: # if one of their matches does not already have a match..
                        maleIndexes[maleIndex] = femaleIndex
                        femaleIndexes[femaleIndex] = maleIndex

                        self.efficientCombos(maleIndexes, femaleIndexes)

                        # don't need to reset maleIndex, since it will be changed again next loop or after exiting
                        femaleIndexes[femaleIndex] = -1

                maleIndexes[maleIndex] = -1
        if nuMatched == 0:
            # every male was matched up - meaning we have a possible solution, let's add it
            self.possibilities.append(prevDict)


    def combos(self, prevDict, males, females):
        if (len(males) == 0): # if one is empty, both should be
            self.possibilities.append(prevDict)
        else:
            for maleName in males:
                for femaleName in females:
                    # this part creates far more overhead than I'd like, should be able to optimize later
                    curMales = list(males)
                    curFemales = list(females)
                    curMales.remove(maleName)
                    curFemales.remove(femaleName)
                    curDict = prevDict.copy()
                    curDict[maleName] = femaleName
                    self.combos(curDict, curMales, curFemales)


    def numRemainingCombinations(self):
        return len(self.possibilities)


class Person:
    def __init__(self, name, isMale):
        self.name = name
        self.isMale = isMale
        self.perfectMatch = None
        self.odds = Odds()

    def setupPartners(self, possibleMatches):
        self.possibleMatches = possibleMatches.copy()

    def hasPerfectMatch(self):
        return self.perfectMatch != None

    def becomeMatched(self, other):
        self.perfectMatch = other
        # clear other matches
        self.possibleMatches = {(other.name, other)}

    def isPerfectMatchWith(self, other):
        return self.hasPerfectMatch() and self.perfectMatch.name == other.name

    def printMatches(self):
        if (self.hasPerfectMatch()):
            print(f'{self.name} is a perfect match with {self.perfectMatch.name}!\n')
        else:
            print(f'{self.name}\'s possible matches:')
            for matchName in self.possibleMatches:
                print(f'{self.name} - {matchName}')
            print('')

    def printOdds(self):
        if (self.hasPerfectMatch()):
            print(f'{self.name} is a perfect match with {self.perfectMatch.name}!\n')
        else:
            print(f'{self.name}\'s possible matches:')
            currentOdds = self.odds.calculateCurrentOdds(self.possibleMatches)
            for matchName in currentOdds:
                print(f'{self.name} - {matchName} - {currentOdds[matchName]}')
            print('')

    def unmatch(self, value):
        if value in self.possibleMatches:
            self.possibleMatches.pop(value)

    def addLightOdds(self, matchName, numerator, divisor):
        self.odds.add(matchName, numerator, divisor)



maleNames = ['Adam', 'Dre', 'Scali', 'Chris T', 'Dillan', 'Ethan', 'Joey', 'JJ', 'Ryan', 'Wes']
males = dict(map(lambda name: (name, Person(name, True)), maleNames))

femaleNames = ['Amber', 'Ashleigh', 'Brittany', 'Coleysia', 'Jacy', 'Jess', 'Kayla', 'Paige', 'Shanley', 'Simone']
females = dict(map(lambda name: (name, Person(name, False)), femaleNames))

for maleName in males:
    males[maleName].setupPartners(females)

for femaleName in females:
    females[femaleName].setupPartners(males)

possibilities = Possibilities(males, females)
print(f'Remaining combinations: {possibilities.numRemainingCombinations()}')

truthBooths = []
truthBooths.append(('Chris T', 'Shanley',  False))
truthBooths.append(('Ethan',   'Jess',     False))
truthBooths.append(('Dillan',  'Jess',     False))
truthBooths.append(('JJ',      'Simone',   False))
truthBooths.append(('Dre',     'Ashleigh', False))
truthBooths.append(('Dillan',  'Coleysia', True))
truthBooths.append(('Chris T', 'Paige',    True))
truthBooths.append(('Ryan',    'Kayla',    False))

lights = []
lights.append((2, [('Adam', 'Brittany'), ('Dre', 'Jacy'), ('Scali', 'Ashleigh'), ('Chris T', 'Jess'), ('Dillan', 'Coleysia'), ('Ethan', 'Shanley'), ('Joey', 'Paige'), ('JJ', 'Simone'), ('Ryan', 'Amber'), ('Wes', 'Kayla')]))
lights.append((4, [('Adam', 'Shanley'), ('Dre', 'Ashleigh'), ('Scali', 'Simone'), ('Chris T', 'Paige'), ('Dillan', 'Jess'), ('Ethan', 'Amber'), ('Joey', 'Brittany'), ('JJ', 'Jacy'), ('Ryan', 'Kayla'), ('Wes', 'Coleysia')]))
lights.append((2, [('Adam', 'Brittany'), ('Dre', 'Ashleigh'), ('Scali', 'Paige'), ('Chris T', 'Simone'), ('Dillan', 'Coleysia'), ('Ethan', 'Amber'), ('Joey', 'Shanley'), ('JJ', 'Jess'), ('Ryan', 'Kayla'), ('Wes', 'Jacy')]))

# lights.append((2, [('Adam', ''), ('Dre', ''), ('Scali', ''), ('Chris T', ''), ('Dillan', ''), ('Ethan', ''), ('Joey', ''), ('JJ', ''), ('Ryan', ''), ('Wes', '')]))



for i in range(0, min(lastIndex, len(truthBooths))):
    (pairMaleName, pairFemaleName, isPerfectMatch) = truthBooths[i]
    pairMale = males[pairMaleName]
    pairFemale = females[pairFemaleName]
    # male.printMatches()
    # female.printMatches()

    if isPerfectMatch:
        pairMale.becomeMatched(pairFemale)
        pairFemale.becomeMatched(pairMale)

        for mName in males:
            males[mName].unmatch(pairFemaleName)
        for fName in females:
            females[fName].unmatch(pairMaleName)
    else: # no match.. :(
        pairMale.unmatch(pairFemaleName)
        pairFemale.unmatch(pairMaleName)


# handle [0-lastIndex] lights
for i in range (0, min(lastIndex, len(lights))):
    (unknownLights, testedMatches) = lights[i]
    possibleMatches = 10 ## will decrement as 'wrong' matches are discovered

    toExamine = []

    for (maleMatchName, femaleMatchName) in testedMatches:
        maleMatch = males[maleMatchName]
        femaleMatch = females[femaleMatchName]

        if maleMatch.isPerfectMatchWith(femaleMatch):
            # treat this case as a known, can disregard 1 light
            unknownLights -= 1
            possibleMatches -= 1
        elif femaleMatchName in maleMatch.possibleMatches:
            # matches are reciprocal, only have to check one
            # these are possible, let's look at the odds after seeing all couples
            toExamine.append((maleMatch, femaleMatch))
        else:
            # can't be a match
            possibleMatches -= 1

    print(f'{unknownLights} of the next {len(toExamine)} are matches!')

    divisor = len(toExamine)
    # print(unknownLights)
    # print(divisor)
    odds = (unknownLights * 100.0) / divisor # assuming an even distribution across all matched couples
    for (maleMatch, femaleMatch) in toExamine:
        print(f'{maleMatch.name} and {femaleMatch.name} have {odds}% of being a match')
        if (odds == 0):
            maleMatch.unmatch(femaleMatch.name)
            femaleMatch.unmatch(maleMatch.name)
        else:
            maleMatch.addLightOdds(femaleMatch.name, unknownLights, divisor)


for maleName in males:
    # males[maleName].printMatches()
    males[maleName].printOdds()



# other notes
# secondary group (either males or females, arbitrary) doesn't need to be tracked, as all relationships are
# reciprocal and displayed on one group as the other. Primary group can track everything
