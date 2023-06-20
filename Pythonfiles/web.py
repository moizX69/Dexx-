import wikipedia

def getwebrep(query):

    keyword1=query
    output = wikipedia.summary(keyword1, sentences=2)
    return(output)



