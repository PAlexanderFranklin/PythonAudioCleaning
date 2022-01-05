import populateMetaData
import random

speaker = random.choice("ET")

testString = (speaker + "M0" + str(random.randint(1,9))
    + str(random.randint(0,2)) + str(random.randint(0,9)) + "21")

userInput = input("Press enter to test with " + testString
    + " or type a test input yourself:")

if userInput:
    testString = userInput

populateMetaData.addDBEntry(testString)