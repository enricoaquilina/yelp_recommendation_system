from nltk.sentiment.vader import SentimentIntensityAnalyzer


test_data_list = ["This movie gave the same vibe as watching/reading Detective Conan, I loike ;)",
                "What?  Inspector Poirot?  I never thought I'd see the day.  I thought he'd be shorter.",
                "I remember watching this film already but in japanese version, the original one, all these in the train is the killers",
                "Where's Sam Jackson?",
                "The song at the end didnt work. Try again.",
                "johnny depp is the victim??",
                "They gotta be in the train where it happen",
                "So it is the board game Cluedo on a train. Also isn't it obvious that Depp is the murderer?? A guy dressed in dark clothing with scars on his face looking at a woman walking towards him alone in a narrow corridor. That is classic evil guy does evil things. Also terrible song choice for this kind of trailer",
                "IDIOTIC MUSIC CHOICE",
                "moustache is the killer",
                "Was so sure Johnny was going to be Poirot, glad I was wrong.",
                "Wow! Johnny looks young again!"]

# def get_all_comments():
#
#     comments = []
#     graph = startConnection()
#
#     comment_list = graph.match(rel_type=YOUTUBE_COMMENT)
#
#     for rel in comment_list:
#         #print rel
#         comment = rel["commentText"].replace("\n", " ")
#         comments.append(comment)
#
#
#     #for cmt in comments:
#     #    print "(\"%s\", \"\"),\n" % cmt
#
#     # train = [("Great place to be when you are in Bangalore.", "pos"),
#     #          ("The place was being renovated when I visited so the seating was limited.", "neg"),
#     #          ("Loved the ambience, loved the food", "pos"),
#     #          ("The food is delicious but not over the top.", "neg"),
#     #          ("Service - Little slow, probably because too many people.", "neg"),
#     #          ("The place is not easy to locate", "neg"),
#     #          ("Mushroom fried rice was spicy", "pos"),
#     #          ]
#     train = [
#         ("Why do we need another book of life ?", ""),
#         ("So The Book of Life, but disney made it, so more people are gonna watch it.", ""),
#         ("it looks like the book of life", ""),
#         ("Reminded me of Spirited Away", ""),
#         ("Nothing spectacular except the look of the city which doesn't have all of those floating hot-air balloons ala 'The Book of Life'.",""),
#         ("this is just like the movie: The Book Of Life", ""),
#         ("So similar to the movie The Book of Life", ""),
#         ("a mexican boy want to cross the other world. Hope no Donald stop him...", ""),
#         ("More contents in this trailer. Look forward!", ""),
#         ("It reminds me Corpse Bride rather than others", ""),
#         ("When I saw the thumbnail I thought it was the book of life", ""),
#         ("Le van a dar un coco por pendejo", ""),
#         ("The only part that looks similar to the book of life is the very beginning", ""),
#         ("No one, huh? Manolo was there before...", ""),
#         ("great theme.....", ""),
#         ("The Book of Life 2 looks great.", ""),
#         ("Did disney just rip off book of life? wtf dude.", ""),
#         ("SO many Book of Life comparisons here, but has anyone even realized this is an ENTIRELY different story!?", ""),
#         ("Disney's The Book of Life...a completely original idea.", ""),
#         ("the new book of life 2 looks good...............      wait", ""),
#         ("book of life copycat", ""),
#         (
#         "I'm so excited for this movie!And I don't love it, just because I'm mexican , I love it just for the simple reason that it's a pixar movie, represents a not very  known culture and because it has a beautiful animation 7u7! PD: Sorry for my english.",
#         ""),
#         ("Isn't this the book of life??", ""),
#         ("I know I'm late but Pixar's the book of life", ""),
#         ("But this is VEERY SAD! All his family is DEAD!! :(", ""),
#         (
#         "dia de los muertos is a 2 day celebration also this movie was made by white people and the book of life was made by latinx people dont @ me",
#         ""),
#         ("This trailer reminds me about the book of life it's almost similar", ""),
#         ("Hmmm..... deathtopia ?", ""),
#         ("this score is so dope", ""),
#         ("this is a totally different one", ""),
#         ("I'm never really sure about if i should watch these on Spanish or in original English...", ""),
#         ("The book of life", ""),
#         ("Ripoff of the Book of Life", ""),
#         ("I don't know why, but in the beginning when he said World, all i could think about is (using epic trailer voice) In a world", ""),
#         ("All I have to say is The Book of Life!!!", ""),
#         ("WTF is with this song?!", ""),
#         ("Might as well release this straight to DVD because it will make nothing at the box office.", ""),
#         ("whats the song 1:44", ""),
#         ("Type cast as a Queen/Princess, who will have an issue with that...", ""),
#         ("Totally nailed the atmosphere and the characters ... NOT", ""),
#         ("A murder mystery where people are confined to an indoor location surrounded by snow. Sounds familiar...", ""),
#         ("This looks good... The music choice is great !", ""),
#         ("hope this is the new usual suspects", ""),
#         ("this doesn't look as good as the poirot version", ""),
#         ("Woah I've actually read this one XD", ""),
#         ("I'm a simple woman. I see Johnny Depp - I click", ""),
#         ("Sherlock?", "neu"),
#         ("A remake of CLUE? Hmmm interesting", "pos"),
#         ("Clue 2: Who Killed Johnny Depp?", "neu"),
#         ("For a secound Ithought this was a sequel to mortdecai.", "neg"),
#         ("John's Wedding: The movie.  Sherlock fans know.", "neg"),
#         ("I would like to never imagine any dragons of any sort.", "neg"),
#         ("Spoiler :  Everyone is the killer .", "neu"),
#         ("this is what movie trailers should be like. short, suspenseful, leaves you wanting more", "pos"),
#         ("And the comedy tour from Ridley Scott continues, with him being the only one not in on his own jokes.", "neg"),
#         ("Spoiler Alert:  They all did it :3", "neg"),
#         ("Still not convinced that the detective is not Pierce Brosnan.", "neg"),
#         ("Daisy Ridleys in this? Now I have to see it", "pos"),
#         ("i t  was  the  count. boom", "neg"),
#         ("Great french/belgian accent.", "pos"),
#         ("the doctor did it", "neg"),
#         ("Cluedo - The Movie", "neg"),
#         (
#         "Black guy shoehorned as a doctor, and they're almost always cast as doctors in films and tv shows these days. Not to mention forcing a WF/BM relationship in the film, making it pretty clear seeing how Daisy was eyeing that flat-nosed chimpanzee.",
#         "neg"),
#         ("The cast is out of this world", "pos"),
#         ("spoilers: the mustache is the murderer", "neg"),
#         ("the original movie is so good", "pos"),
#         ("I have been begging for a murder mystery in such a long time. I seeing this the moment it comes out.", "pos"),
#         ("watch a kind of the same thing on doctor who ages ago.", "neg"),
#         ("That cast though", "pos"),
#         ("Clue the movie.", "neu"),
#         ("It's Clue on a train! i would guess it would be the detective or johhny depp as the murderer", "neu"),
#         ("Could be a great film, rotten trailer", "neg"),
#         ("Obviously the butler did it.", "neu"),
#         ("I just hope that the H.H Holmes movie The Devil in the white city that also will be about murder obviously will come out soon or atleast that DiCaprio and Scorsese will start working soon I feel like that movie will be a way better mystery, crime, murder movie",
#         "neu"),
#         ("They had me until the mustache.", "neg"),
#         ("Was I the only one who didn't see johnny depp", "neu"),
#         ("Who are you?  Hercule Poirot! Who?  I am Hercule Poirot man...legendary detective....guys..... ah, forget this!",
#         "neu"),
#         ("This movie looks interested", "pos"),
#         ("Gilderoy's done with stealing other wizards secrets and now he's probably stealing Sherlock's identity.", "neu"),
#         ("Kickass moustaches!", "pos"),
#         ("I see Johnny Depp I like", "pos"),
#         ("i hope it does the book justice", "pos"),
#         ("Cluedo looks cool", "pos"),
#         ("So they killed Depp. He's basically just for trailers like James Franco in Alien: Covenant?", "neu"),
#         ("Johnny Depp YAAAAAAAAAAAAAAAAASSSSS", "pos"),
#         ("damm interesting!! can get that best screenplay if done right with all those actors! but the song tho what the heck lol",
#         "pos"),
#         ("The song at the end ruined it for me...", "neg"),
#         ("Was johnny the one who died?", "neu"),
#         ("easy: Johnny Depp is the murderer.", "neu"),
#         ("Strange music choice, but it looks great nonetheless.", "pos"),
#         ("Oh look it's that one adventure time episode 'Mystery Train'", "neg"),
#         ("They all take part killing the victim. Everyone stabs him one by one so the depth is different.", "neg"),
#         ("When will this obsession with making everything hard and street end?  It's ruining trailers.", "neg"),
#         ("maybe the oldest spoiler in the world but still: they all did it.", "neu"),
#         ("Why why this song? Imagine Dragons in a movie trailer today is the equivalent of putting Who Let the Dogs Out in a trailer in the early 2000s...",
#         "neg"),
#         ("I really like the book, hope the movie won't suck", "neu"),
#         ("and the most modest in the world also...", "neu"),
#         ("looks great, but david suchet will always be poirot for me", "pos"),
#         ("Modern songs in period piece movies make no sense.", "neg"),
#         ("why don't people like the song for the trailer? I loved it hahaha MICHELLE PFEIFFER!!!!!!!!!!", "pos"),
#         ("This is Jack Sparrow generation", "pos"),
#         ("What a weird music choice", "neg"),
#         ("Great song, terrible for this trailer", "neu"),
#         (
#         "The all were involved in the murder.  All are connected to the dead. Poirot let's them go.  Thank me later,  I saved you $10.",
#         "neu"),
#         ("So based on that shot with the rundown on everyone I guess Johnny Depp is the one who gets murdered.", "neu"),
#         ("Y did it look like a new fantastic beasts and we're to find them trailer", "neu"),
#         ("Wat?", "neg"),
#         ("Everything but the moustaches. Someone should have vetoed those.", "neu"),
#         (
#         "EXCELLENT MAN ...We need Different kind Movie like THIS ...wow Its going to do Excellent Box Office at OVERSEAS if it received a great rating in ROTTEN 80+",
#         "pos"),
#         ("'demons' would be a better choice for this particular I think ...though I really like this song too ...", "pos"),
#         ("The end of the trailer was pretty lame, but it got me interested enough to check it out.", "pos"),
#         ("Then I heard Imagine Dragon's Believer...", "neg"),
#         ("Reminds me of Adventure time :D", "pos"),
#         (
#         "Song choice ruined the vibe. They should honestly release the exact same trailer, but with the actual theme of the movie, not a popsong",
#         "neu"),
#         ("Is this based on room escape", "neu"),
#         ("I was excited... not so much now... maybe it was the song, just something put me off.", "neg"),
#         ("That moustache...", "neg"),
#         ("I Must-ache (must ask) you Detective, How did you grow it Like That?!", "neu"),
#         ("Remakes, remakes, remakes shhhhiiiisssshhhh", "neg"),
#         (
#         "I definitely recommend reading the book before watching the movie. And may I add that this trailer had a pretty shitty song choice",
#         "neg"),
#         ("Branagh's terrible accent ranks up there with Steve Martins Inspector Clouseau.", "neg"),
#         ("I'm most excited for sergei polunin and Leslie odom jr", "pos"),
#         ("Jonny Depp with the masonic one eye symbolism did it", "pos"),
#         ("So Clue?", "neu"),
#         ("The killer is Johnny depp", "neu"),
#         (
#         "If I didn't know any better, I would think that Imagine Dragon's soul occupation was to make movie trailer music.",
#         "neu"),
#         ("Bookmark this video for Common mistakes for picking trailer music lesson in marketing.", "neg"),
#         ("That cast though!  My God! Definitely seeing this, and I hope that Depp has a prominent role in this like Branagh and the rest.", "pos"),
#         ("I'm disappointed I believe that at the end he went to say, phin and jake", "neg"),
#         ("Another movie on Agatha Christie novel. Cool.", "pos"),
#         ("Looks awful. I hope its not.", "neg")
#     ]
#
#     # Step 2
#     dictionary = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
#
#     # Step 3
#     t = [({word: (word in word_tokenize(x[0])) for word in dictionary}, x[1]) for x in train]
#
#     # Step 4 the classifier is trained with sample data
#     classifier = nltk.NaiveBayesClassifier.train(t)
#
#     test_data = "Manchurian was hot and spicy"
#
#
#
#     for test_data in test_data_list:
#         test_data_features = {word.lower(): (word in word_tokenize(test_data.lower())) for word in dictionary}
#
#         print test_data + ": " + (classifier.classify(test_data_features)) + " prob pos: " + str((classifier.prob_classify(test_data_features).prob('pos')))\
#               + " prob neg: " + str(classifier.prob_classify(test_data_features).prob('neg')) + " prob neu: " + str(classifier.prob_classify(test_data_features).prob('neu'))
#
#     return comments
#for testing only
def vader_sentiment():
    test_data_list = ["This movie gave the same vibe as watching/reading Detective Conan, I loike ;)",
                      "What?  Inspector Poirot?  I never thought I'd see the day.  I thought he'd be shorter.",
                      "I remember watching this film already but in japanese version, the original one, all these in the train is the killers",
                      "Where's Sam Jackson?",
                      "The song at the end didnt work. Try again.",
                      "johnny depp is the victim??",
                      "They gotta be in the train where it happen",
                      "So it is the board game Cluedo on a train. Also isn't it obvious that Depp is the murderer?? A guy dressed in dark clothing with scars on his face looking at a woman walking towards him alone in a narrow corridor. That is classic evil guy does evil things. Also terrible song choice for this kind of trailer",
                      "IDIOTIC MUSIC CHOICE",
                      "moustache is the killer",
                      "Was so sure Johnny was going to be Poirot, glad I was wrong.",
                      "Wow! Johnny looks young again!"]

    sid = SentimentIntensityAnalyzer()
    for cmt in test_data_list:
        print("-----------------\n%s\n" % cmt)
        ss = sid.polarity_scores(cmt)
        for k in ss:
            print('{0}: {1}, '.format(k, ss[k]))
            print()


def get_sentiment_analyzer():
    return SentimentIntensityAnalyzer()


# return 1 for pos, 0 for neutral, -1 for neg
def get_sentiment_polarity(comment):
    analyser = get_sentiment_analyzer()
    ss = analyser.polarity_scores(comment)

    largest = ""
    if ss['neg'] > ss['neu']:
        largest = "neg"
    else:
        largest = "neu"

    if ss['pos'] > ss[largest]:
        largest = "pos"

    if largest == "pos":
        return 1
    elif largest == "neg":
        return -1
    elif largest == "neu":
        return 0


# if polarity is positive return the sentiment score by the sentiment analysis
# if polarity is negative return the sentiment score by the sentiment analysis
# if neutral return 0
# for sentiment score do not return actual decimal number
# since results are between 0 and 1 for both negative and positive
# get the positive score if it is positive, multiple by 10 (0.76543 -> 7.6543)
# round number to integer, such that we create a 'rating' scale from -10 to 10, with 0 being neutral
# sentiment int is updated such that, very negative sentiments are changed to rating 1, mild negative
# (0.3 till 0.6) as 2
# neutral as 3, mild positive 4 and positive 5 such that these are coherent with normal movie ratings

def get_sentiment_score(comment, polarity):
    analyser = get_sentiment_analyzer()
    ss = analyser.polarity_scores(comment)

    if polarity == 1:
        sentiment = ss['pos']
        sentiment = sentiment * 10
        sentiment_int = int(round(sentiment))

        rating = 4
        # if sentiment_int >= 3 and sentiment_int <= 6:
        #    rating = 4
        if sentiment_int >= 7:
            rating = 5
        print("sentiment" + str(sentiment) + " sentiment int " + str(sentiment_int) + " rating " + str(rating))
        return rating
    elif polarity == -1:
        sentiment = ss['neg']
        sentiment = sentiment * -10
        sentiment_int = int(round(sentiment))

        rating = 2
        # if sentiment_int <= -3 and sentiment_int >= -6:
        #    rating = 2
        if sentiment_int <= -7:
            rating = 1
        print("sentiment" + str(sentiment) + " sentiment int " + str(sentiment_int) + " rating " + str(rating))
        return rating
    else:
        return 3