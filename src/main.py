import argparse
import pandas


parser = argparse.ArgumentParser(description='Generate possible combinations for MTV\'s Are You The One :).')
parser.add_argument('season', help='the path to a season directory in the resources directory')
args = parser.parse_args()

seasonDirectory = f'resources/{args.season}/'
maleNames = []
femaleNames = []
truthBooths = []
lights = []

names = pandas.read_csv(f'{seasonDirectory}names.csv')
for index, row in names.iterrows():
    if row['sex'] == 'F':
        femaleNames.append(row['name'])
    else:
        maleNames.append(row['name'])

truthBoothDF = pandas.read_csv(f'{seasonDirectory}truthBooths.csv')
for index, row in truthBoothDF.iterrows():
    truthBooths.append(row)

lightDF = pandas.read_csv(f'{seasonDirectory}lights.csv')
for index, row in lightDF.iterrows():
    numLights = row['lights']
    pairs = []
    for i in range(0, len(maleNames)):
        pairs.append((row[f'm{i}'], row[f'f{i}']))
    lights.append((numLights, pairs))


class Possibilities:

    def __init__(self, males, females):
        self.possibilities = []
        self.males = males.copy()
        self.females = females.copy()
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
            if self.foundPossibilities % 100000 == 0:
                print(f'{self.foundPossibilities} possibilities found.')

        else:
            self.initialCombinations(currentMaleIndex+1) # move on to find next match

        # don't need to reset maleIndex, since it will be changed again next loop or after exiting
        self.femaleIndexes[currentFemaleIndex] = -1


    def numRemainingCombinations(self):
        return len(self.possibilities)


    def filterPerfectMatch(self, combination, maleIndex, femaleIndex):
        return combination[maleIndex] == femaleIndex

    def filterFailedMatch(self, combination, maleIndex, femaleIndex):
        return combination[maleIndex] != femaleIndex


    def truthBoothPerfectMatch(self, maleIndex, femaleIndex):
        self.possibilities = list(filter(lambda combination: self.filterPerfectMatch(combination, maleIndex, femaleIndex), self.possibilities))

    def truthBoothFailedMatch(self, maleIndex, femaleIndex):
        self.possibilities = list(filter(lambda combination: self.filterFailedMatch(combination, maleIndex, femaleIndex), self.possibilities))


    def filterLights(self, combination, lightMatchups, numLights):
        for index in range(0, self.numMales):
            # print(f'index = {index}, lightMatchups[index] = {lightMatchups[index]}, combination[index] = {combination[index]}')
            if lightMatchups[index] == combination[index]:
                # print(f'decrementing {numLights}')
                numLights -= 1
                if numLights < 0: # if we've already exceeded our limit, just go ahead and return false
                    return False

        # print(f'numLights: {numLights}')
        return numLights == 0 # if number of found matches turned expectedCount exactly to 0, this situation is possible

    def updateLights(self, lightMatchups, numLights):
        self.possibilities = list(filter(lambda combination: self.filterLights(combination, lightMatchups, numLights), self.possibilities))

    def getAllProbabilities(self):
        probabilities = []
        finalProbabilities = []

        for i in range(0, self.numMales):
            probabilities.append({})
            finalProbabilities.append({})

        for poss in self.possibilities:
            for maleIndex in range(0, self.numMales):
                femaleIndex = poss[maleIndex]
                if femaleIndex not in probabilities[maleIndex]:
                    probabilities[maleIndex][femaleIndex] = 1
                else:
                    probabilities[maleIndex][femaleIndex] += 1

        divisor = self.numRemainingCombinations()

        for maleIndex in range(0, self.numMales):
            for femaleIndex in probabilities[maleIndex]:
                finalProbabilities[maleIndex][femaleIndex] = (probabilities[maleIndex][femaleIndex] * 1.0) / divisor

        return finalProbabilities

    def printAllProbabilities(self):
        probs = self.getAllProbabilities()
        for maleIndex in range(0, self.numMales):
            maleProbs = probs[maleIndex]
            if (len(maleProbs) == 1):
                print(f'{self.males[maleIndex]} is a perfect match with {self.females[0]}!\n')
            else:
                print(f'{self.males[maleIndex]}\'s possible matches:')
                for femaleIndex in maleProbs:
                    print(f'{self.males[maleIndex]} - {self.females[femaleIndex]} - {maleProbs[femaleIndex]}')
                print('')



maleIndexMap = {} ## this can be moved to probabilities
for maleIndex in range(0, len(maleNames)):
    maleIndexMap[maleNames[maleIndex]] = maleIndex

femaleIndexMap = {}
for femaleIndex in range(0, len(femaleNames)):
    femaleIndexMap[femaleNames[femaleIndex]] = femaleIndex

possibilities = Possibilities(maleNames, femaleNames)
print(f'Remaining combinations: {possibilities.numRemainingCombinations()}')


# handle [0-lastIndex] lights
for i in range (0, min(len(truthBooths), len(lights))):
    ## handle truth booths
    maleMatchName = truthBooths[i].maleName
    femaleMatchName = truthBooths[i].femaleName
    isPerfectMatch = truthBooths[i].isMatch
    pairMale   = maleIndexMap[maleMatchName]
    pairFemale = femaleIndexMap[femaleMatchName]

    if isPerfectMatch:
        possibilities.truthBoothPerfectMatch(pairMale, pairFemale)
    else: # no match.. :(
        possibilities.truthBoothFailedMatch(pairMale, pairFemale)

    print(f'After truth booth {i} - remaining combinations: {possibilities.numRemainingCombinations()}')

    ## handle lights
    (numLights, testedMatches) = lights[i]

    lightIndexes = {}

    for (maleMatchName, femaleMatchName) in testedMatches:
        pairMale   = maleIndexMap[maleMatchName]
        pairFemale = femaleIndexMap[femaleMatchName]
        lightIndexes[pairMale] = pairFemale

    possibilities.updateLights(lightIndexes, numLights)

    print(f'Night {i} - remaining combinations: {possibilities.numRemainingCombinations()}')



print(f'Final remaining combinations: {possibilities.numRemainingCombinations()}')

possibilities.printAllProbabilities()
