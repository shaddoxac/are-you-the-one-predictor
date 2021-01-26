lastIndex = 10 ## will go through at most the first {lastIndex} days

class Possibilities:

    def __init__(self, males, females):
        self.possibilities = []
        self.males = males
        self.females = females
        self.numMales = len(males)
        self.numFemales = len(females)
        self.foundPossibilities = 0

        self.maleIndexes   = [-1] * self.numMales
        self.femaleIndexes = [-1] * self.numFemales
        self.initialCombinations(0)


    def initialCombinations(self, currentMaleIndex):
        for currentFemaleIndex in range(0, self.numFemales): # find all possible female matches for this male that aren't already taken
            if self.femaleIndexes[currentFemaleIndex] == -1: # if one of their possible matches does not already have a match..
                self.initialCombinationsPair(currentMaleIndex, currentFemaleIndex)

        self.maleIndexes[currentMaleIndex] = -1

    def initialCombinationsPair(self, currentMaleIndex, currentFemaleIndex):
        self.maleIndexes[currentMaleIndex] = currentFemaleIndex
        self.femaleIndexes[currentFemaleIndex] = currentMaleIndex

        if currentMaleIndex+1 == self.numMales: # every male was matched up - meaning we have a possible solution, let's add it

            self.possibilities.append(self.maleIndexes.copy())
            self.foundPossibilities += 1
            if self.foundPossibilities % 10000 == 0:
                print(f'{self.foundPossibilities} possibilities found.')

        else:
            self.initialCombinations(currentMaleIndex+1) # move on to find next match

        # don't need to reset maleIndex, since it will be changed again next loop or after exiting
        self.femaleIndexes[currentFemaleIndex] = -1


    def numRemainingCombinations(self):
        return len(self.possibilities)


    def filterPerfectMatch(self, combination, maleIndex, femaleIndex):
        combination[maleIndex] == femaleIndex

    def filterFailedMatch(self, combination, maleIndex, femaleIndex):
        combination[maleIndex] != femaleIndex


    def truthBoothPerfectMatch(self, maleIndex, femaleIndex):
        self.possibilities = filter(lambda combination: self.filterPerfectMatch(combination, maleIndex, femaleIndex), self.possibilities)

    def truthBoothFailedMatch(self, maleIndex, femaleIndex):
        self.possibilities = filter(lambda combination: self.filterFailedMatch(combination, maleIndex, femaleIndex), self.possibilities)


    def filterLights(self, combination, lightMatchups, numLights):
        for index in range(0, self.numMales):
            if lightMatchups[index] == combination[index]:
                numLights -= 1
                if numLights < 0: # if we've already exceeded our limit, just go ahead and return false
                    return False

        return numLights == 0 # if number of found matches turned expectedCount exactly to 0, this situation is possible

    def updateLights(self, lightMatchups, numLights):
        self.possibilities = filter(lambda combination: self.filterLights(combination, lightMatchups, numLights), self.possibilities)

    def getAllProbabilities(self):
        probabilities = [{}] * self.numMales
        for poss in self.possibilities:
            for maleIndex in poss:
                if femaleIndex not in probabilities[maleIndex]:
                    probabilities[maleIndex][femaleIndex] = 1
                else:
                    probabilities[maleIndex][femaleIndex] += 1

        finalProbabilities = []
        divisor = self.numRemainingCombinations()

        for prob in probabilities:
            finalProbabilities.append(map(prob, lambda numMatches: numMatches * 1.0 / divisor))

        return finalProbabilities

    def printAllProbabilities(self):
        probs = self.getAllProbabilities()
        for maleIndex in range(0, self.numMales):
            maleProbs = probs[maleIndex]
            if (len(maleProbs) == 1):
                print(f'{self.males[maleIndex]} is a perfect match with {self.females[0]]}!\n')
            else:
                print(f'{self.males[maleIndex]}\'s possible matches:')
                for femaleIndex in maleProbs:
                    print(f'{self.males[maleIndex]} - {self.females[femaleIndex]} - {maleProbs[femaleIndex]}')
                print('')

class Person:
    def __init__(self, name, isMale):
        self.name = name
        self.isMale = isMale
        self.perfectMatch = None

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
            currentOdds = self.calculateCurrentOdds(self.possibleMatches)
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
maleIndexMap = {} ## this can be moved to probabilities
for maleIndex in range(0, len(males)):
    maleIndexMap[maleNames[maleIndex]] = maleIndex

femaleNames = ['Amber', 'Ashleigh', 'Brittany', 'Coleysia', 'Jacy', 'Jess', 'Kayla', 'Paige', 'Shanley', 'Simone']
females = dict(map(lambda name: (name, Person(name, False)), femaleNames))
femaleIndexMap = {}
for femaleIndex in range(0, len(females)):
    femaleIndexMap[femaleNames[femaleIndex]] = femaleIndex


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
    pairMale   = maleIndexMap[pairMaleName]
    pairFemale = femaleIndexMap[femalePairName]

    if isPerfectMatch:
        possibilities.truthBoothPerfectMatch(pairMale, pairFemale)
    else: # no match.. :(
        possibilities.truthBoothFailedMatch(pairMale, pairFemale)

    print(f'Remaining combinations: {possibilities.numRemainingCombinations()}')


# handle [0-lastIndex] lights
for i in range (0, min(lastIndex, len(lights))):
    (lights, testedMatches) = lights[i]

    lightIndexes = []

    for (maleMatchName, femaleMatchName) in testedMatches:
        pairMale   = maleIndexMap[pairMaleName]
        pairFemale = femaleIndexMap[femalePairName]
        lightIndexes.append((pairMale, pairFemale))

    possibilities.updateLights(lightIndexes, lights)

    print(f'Remaining combinations: {possibilities.numRemainingCombinations()}')



print(f'Remaining combinations: {possibilities.numRemainingCombinations()}')
