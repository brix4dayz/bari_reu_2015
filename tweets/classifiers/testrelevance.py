import tweetclassifier as tc
import twittercriteria as twc
import numpy as np
import matplotlib.pyplot as plt

testRelevant = None
testIrrelevant = None

trainingPaths = {'relevant':'/relevantTraining.txt', 'irrelevant':'/irrelevantTraining.txt'}

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
        "boston, what is going on? #prayforbostom #mitshooting",
        "#watertown stay vigilant, there is no where for this asshole to go. each minute that goes by they are closer to finding him.",
        "boston is all fucked up and shut down to lockdown died not a soul in sight they need to catch the 2nd suspect #watertown",
        "video of the explosion taken from the finish line. just horrible.",
        "@dailystarnews: boston marathon bombings kill 3, hurt over 100 "]

    testIrrelevant = ["it\'s not a #bostonmarathon until @theeisnotsilent has stolen cheese off a stranger\'s duck plate on their front lawn.",
        "sir, the cowbell around your neck is unnecessary. #bostonmarathon",
        "matches the hair @theeisnotsilent #bostonmarathon",
        "@kyle_kysmitty @teamhendrick @jeffgordonweb @kansasspeedway. thats the distance of the marathon, 26.2 miles.  thank you hms.",
        "sitting on the #mbta watching marathon runners go by, i can't believe rosie ruiz got ahead of the pack on this slow-ass train.",
        "happy hump day! time to #getnaked drinking a naked hopularity by @slumbrew at @hopsexplosion",
        "good luck to all of those at the boston marathon finish line today. sending love and good thoughts!",
        "praying for good health!!!",
        "love seeing all those marathon runners rocking their jackets",
        ".2 to go #youcandoit @ almost the finish line ",
        "#marathonmonday #gocrazy #cheerloud @go4th_",
        "i'm at not your average joe's - @nyajoes (watertown, ma)",
        "midnight marathon bike ride ",
        "it's good to be home. #bostonstrong @ fenway park ",
        "happy birthdayyy @jordancollier23"]
    return

# def scoreMND(chiK):
#     initTests()
#     clssr = rc.RelevanceMNB(chiK)
#     clssr.test(testRelevant, testIrrelevant)
#     return clssr.balancedF()

def testRelevantClassifier(clssr):
    initTests()
    print "Testing " + type(clssr).__name__ + "..."
    rel = clssr.classify(testRelevant)
    irr = clssr.classify(testIrrelevant)
    trueRel = np.empty(len(rel))
    trueRel.fill(0)
    trueIrr = np.empty(len(irr))
    trueIrr.fill(1)
    print clssr.getConfusionMatrix(np.append(trueRel, trueIrr), np.append(rel, irr))
    print "...done.\n"      

relClssr = tc.TweetClassifierMNB(trainingPaths, twc.cleanUpTweet)

testRelevantClassifier(relClssr)

relClssr = tc.TweetClassifierSVM(trainingPaths, twc.cleanUpTweet)

testRelevantClassifier(relClssr)

# relClssr = tc.TweetClassifier(trainingPaths, twc.cleanUpTweet)

# testRelevantClassifier(relClssr)

# print len(clsrNB.wordFeatures)

# chis = range(1000, len(clsrNB.wordFeatures)+1, 2)

# fs = []

# for c in chis:
#     fs.append(scoreMND(c))

# chis = np.array(chis)
# fs = np.array(fs)

# bestF = np.amax(fs)
# bestChi = chis[np.argmax(fs)]

# print bestF
# print bestChi

# plt.plot(chis, fs, 'b')
# plt.plot(bestChi, bestF, '^g')

# plt.show()

#clsrSVM = rc.RelevanceSVM()
