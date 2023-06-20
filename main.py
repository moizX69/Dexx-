from flask import Flask, render_template, request
import website as w
import os
from py2neo import Graph,Node
from website import auth,database
from gingerit.gingerit import GingerIt
from pyaiml21 import Kernel
import nltk as nl
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from glob import glob
from web import getwebrep
from collections import Counter
import pytholog as pl
from prolog import getfact
graph = Graph("bolt://localhost:7687", auth=("neo4j", "moiz11..."))
sia = SentimentIntensityAnalyzer()
parser = GingerIt()
app = w.creat_app()
nouns=['NN', 'NNS', 'NNP', 'NNPS']
relations=["friend","son_of","relative"]
relnl=["father",'friend','mother','son','relative','relatives','friends']
def checkvb(pos):
    check=False
    for t in pos:
        if t[1] == "VB":
            check=True

    return check


def cn(pos,words):
    noun=" "
    for t in pos:
        if t[1] in nouns:
            noun= t[0]


    return noun





bot = Kernel()
path1 = r"C:\Users\Laptop Ally\PycharmProjects\Dexx\data"
list1=["Bye","Good Bye","See you later","See Yaa"]
txt=""
whfam=['who','whom','what','when','where','which','why','whose','how','could','would','do','does','should','was','were','is','am','are','will','shall']
clist=[]

def find_most_occurring_element(lst):
    counter = Counter(lst)
    most_common_element = max(counter, key=counter.get)
    return most_common_element



def getknowns(email):
    known = []
    checkip = database.get_ip(email)
    users = graph.run("""MATCH(n) return n.ip,n.email """).data()

    sep1 = checkip.split(".")
    netid1 = sep1[0:3]

    for i in users:
        sep = i['n.ip'].split(".")
        netid = sep[0:3]

        if (netid == netid1 and i['n.email'] != email):
            known.append((i["n.email"]))

    names=[]
    for i in known:
        names.append(database.get_name(i))


    return names

def getdef(pos,words):
    noun = cn(pos, words)
    if noun != " ":
        s = wordnet.synsets(noun)
        s = wordnet.synset(noun + ".n.01").definition()
        response = s
    return response


def getstype(words,query,pos):
    if words[0].lower() in whfam or query.strip().endswith("?"):
        stype = "Question"
    elif "!" in query:
        stype = "Exclamatory"
    elif checkvb(pos):
        stype = "Order"
    else:
        stype = "Statement"
    return stype

def checkwebques(query,stype,words,pos):
    check=False
    if stype == "Question" and pos[-2][1] in nouns and len(words)<7 and "Who is" in query or "What is " in query and "name" not in words and "botmaster" not in words and "my" not in words and "your" not in words and "bot master" not in query:
        check=True
    return check

def getsent(email):
    chat=database.getchat(email)
    sentiment = ""
    s = []

    for i in range(len(clist)-5,len(clist)):
        query=clist[i]
        scores = sia.polarity_scores(query)
        compound_score = scores['compound']
        if compound_score >= 0.05:
             sentiment = "positive"
        elif compound_score <= -0.05:
             sentiment = "negative"
        else:
            sentiment = "neutral"
        s.append(sentiment)

    x = find_most_occurring_element(s)
    sentiment=x

    return sentiment

def getmood(sentiment):
    mood=""
    if sentiment == "positive":
        mood="happy"
    elif sentiment == "negative":
        mood="sad or angry"
    else:
        mood="neutral"
    return mood

def checkipques(query,stype,words):

    check=False

    if stype=="Question" and "my" in query and "IP" in words or"ip address" in query:

        check=True
    return check
for name in glob(path1 + "\*"):
    bot.learn_aiml(name)




@app.route("/get")
def get_bot_response():



    global clist

    response=""
    query = request.args.get('msg')
    que = parser.parse(query)
    query = que["result"]
    email = auth.email6
    name=database.get_name(email)
    gender=database.get_gender(email)
    ip=database.get_ip(email)
    chat=f"\n{name} : "+query
    clist.append(query)

    database.storechat(email, chat)

    b = bot.setBotPredicate("name", "Dexx")

    c = bot.setPredicate("fullname", name)
    c = bot.setPredicate("name",name)
    d = bot.setPredicate("email", email)
    d = bot.setPredicate("gender", gender)
    bot.setBotPredicate("name", "Dexx")
    bot.setBotPredicate("email", "amjadmoiz11@gmail.com")
    bot.setBotPredicate("botmaster", "Moiz")
    bot.setBotPredicate("master", "Moiz")
    bot.setBotPredicate("country", "Pakistan")
    bot.setBotPredicate("nationality", "Pakistani")
    r=f"My name is {name}."
    bot.respond(r,name)
    list1=['son(X,Y):-parent(Y,X)', 'father(X,Y):-parent(X,Y),male(X)', 'mother(X,Y):-parent(X,', 'Y),female(X)', 'grandparent(X,Y):-parent(X,Z),parent(Z,Y)', 'grandfather(X,Y):-grandparent(X,Y),male(X)', 'grandmother(X,Y):-grandparent(X,Y),female(X)', 'husband(X,Y):-son(Z,X),son(Z,Y),male(X)', 'wife(X,Y):-son(Z,X),son(Z,Y),female(X)', 'ancesstor(X,Y):-parent(X,Y)', 'ancesstor(X,Y):-parent(X,Z),ancesstor(Z,Y)', 'brother(X,Y):-parent(Z,X),parent(Z,Y),male(X),X\\==Y', 'sister(X,Y):-parent(Z,X),parent(Z,Y),female(X),X\\==Y', 'mamu(X,Y):-brother(X,Z),mother(Z,Y)', 'chachu(X,Y):-brother(X,Z),father(Z,Y)', 'khala(X,Y):-sister(X,Z),mother(Z,Y)', 'phupho(X,Y):-sister(X,Z),father(Z,Y)']
    sent = nl.sent_tokenize(query)
    words = nl.word_tokenize(query)
    pos = nl.pos_tag(words)
    p1=getfact(sent,words,pos,name)
    fact = p1.pop()
    frel = p1.pop()
    n1 = p1.pop()
    n2 = p1.pop()
    print(fact, n1, n2, frel)

    list1.insert(0, fact)
    newkb = pl.KnowledgeBase("Social Network")
    newkb(list1)

    as1 = newkb.query(pl.Expr(fact))
    print(as1)
    if n2 != name:
        print(1)

        database.new_rel(n2, n1, frel)
    else:
        database.rel(email, n1, frel)






    stype = getstype(words,query,pos,)

    if checkwebques(query,stype,words,pos):
        response = getwebrep(query)

    elif checkipques(query, stype, words):
        response=f"You ip address is {ip}. "
    elif stype=="Question" and "definition of" in query.lower():
        response=getdef(pos,words)


    else:
        response = bot.respond(query, name)


    response2 = " "


    if response and response!="Recursion limit exceeded." and response!="none" and response!="None" and response!=" " and response!="unknown":
        response2=response
        chat = f"\nbot : " + response2

        database.storechat(email, chat)
        return (str(response))
    else:

        known = getknowns(email)

        if(len(known)!=0):

            response2 = f"Do you know {known[0]} ? They are near you"



        elif len(clist)>5:
            print(0)
            sentiment = getsent(email)
            mood=getmood(sentiment)
            if(mood!="neutral"):
                response2=f"You seem {mood} today. How is your day going?"
            else:
                pass


        chat = f"\nbot : " + response2

        database.storechat(email, chat)
        return (str(response2))







if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)



