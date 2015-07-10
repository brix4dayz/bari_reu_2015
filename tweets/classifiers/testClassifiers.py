import relevanceclassifier as rc
import numpy as np
import matplotlib.pyplot as plt

testRelevant = None
testIrrelevant = None

def initTests():
    global testRelevant, testIrrelevant
    testRelevant = ["being 10 miles away from this explosion scares the shit out of me #prayersforboston",
        "ahhh! \"@bostonglobe: breaking news: neighbors say police officers have told them the suspect in the watertown backyard is covered in blood.\"",
        "got him #dontfuckwithboston #bostonpride",
        "@bravoandy was at the marathon monday and on lockdown today. won't stop us from #bostonspiritday #bostonstrong",
        "about #bostonmarathonexplosion: \"@savannahguthrie: fmr atf agent calls these devices \"hellish and diabolical\" in design - on @todayshow\"",
        "thoughts and prayers go out to all those in the explosion #prayforboston",
        "#prayingforboston as i try to sleep tonight, goodnight world. #findpeace",
        "boston bombers are brothers. #watertown #boston",
        "wait it says hes cornered. it says he his cornered #watertown",
        "bomb at the finish line??",
        "boston, what is going on? #prayforbostom #mitshooting"]

    testIrrelevant = ["it\'s not a #bostonmarathon until @theeisnotsilent has stolen cheese off a stranger\'s duck plate on their front lawn.",
        "sir, the cowbell around your neck is unnecessary. #bostonmarathon",
        "matches the hair @theeisnotsilent #bostonmarathon",
        "@kyle_kysmitty @teamhendrick @jeffgordonweb @kansasspeedway. thats the distance of the marathon, 26.2 miles.  thank you hms.",
        "sitting on the #mbta watching marathon runners go by, i can't believe rosie ruiz got ahead of the pack on this slow-ass train.",
        "happy hump day! time to #getnaked drinking a naked hopularity by @slumbrew at @hopsexplosion",
        "good luck to all of those at the boston marathon finish line today. sending love and good thoughts!",
        "praying for good health!!!",
        "watertown chief of police had a very strange interview on cnn today, anyone have an explanation for it?"]
    return

def scoreMND(chiK):
    initTests()
    clssr = rc.RelevanceMNB(chiK)
    clssr.test(testRelevant, testIrrelevant)
    return clssr.balancedF()

def testClassifier(clssr):
    initTests()
    print "Testing " + type(clssr).__name__ + "..."
    clssr.test(testRelevant, testIrrelevant)
    clssr.confusionMatrix()
    print "...done.\n"      


clsrNB = rc.RelevanceClassifier()

testClassifier(clsrNB)

print len(clsrNB.wordFeatures)

chis = range(1000, len(clsrNB.wordFeatures)+1, 2)

fs = []

for c in chis:
    fs.append(scoreMND(c))

chis = np.array(chis)
fs = np.array(fs)

bestF = np.amax(fs)
bestChi = chis[np.argmax(fs)]

print bestF
print bestChi

plt.plot(chis, fs, 'b')
plt.plot(bestChi, bestF, '^g')

plt.show()

#clsrSVM = rc.RelevanceSVM()
