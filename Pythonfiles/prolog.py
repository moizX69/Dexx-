import nltk as nl
import pytholog as pl
from website import database
def getfact(sent,words,pos,name):
    relations=["friend","son_of","relative"]
    relnl=["father",'mother','son','relative','relatives','friend','friends']

    nouns=['NN', 'NNS', 'NNP', 'NNPS']
    crel=""
    frel=""


    ind=0
    if len(words)>3:
      for i in words:
        if i.lower() in relnl:
          crel=i.lower()
          break
        ind+=1
      if crel=="father" or crel=="mother":
        frel="son_of"
      elif crel=='friend'or crel=='friends':
        frel="are_friends"
      elif crel=='relative'or crel=='relatives':
        frel="are_relatives"
      elif crel=="son":
        frel="son_of1"
      ind1=0
      e=[]
      temp=[]

      if frel=="son_of":

        if "my" not in words and words[ind+1].lower() =="of" :

          for i in pos:
            if i[0] not in relnl and i[1] in nouns:
              if ind1<2:

                e.append(i[0])
                ind1+=1
          e[0],e[1]=e[1],e[0]
        else:
           for i in pos:
            if i[0] not in relnl and i[1] in nouns:
              if ind1<2:
                e.append(i[0])
                ind1+=1


      elif frel=="are_friends":
          for i in pos:
            if i[0] not in relnl and i[1] in nouns:
              if ind1<2:
                e.append(i[0])
                ind1+=1
      elif frel=="are_relatives":
          for i in pos:
            if i[0] not in relnl and i[1] in nouns:
             if ind1<2:
                e.append(i[0])
                ind1+=1
      elif frel=="son_of1":
          for i in pos:
            if i[0] not in relnl and i[1] in nouns:
              if ind1<2:
                e.append(i[0])
                ind1+=1

    if frel != "" and len(e) == 0:
        return []
    else:
        if (len(e) == 1):
            p = e.pop()
            e.append(name)
            e.append(p)
            str = f"{frel}({e[0]},{e[1]})"
            e.append(frel)
            e.append(str)
            return e
        elif e!=[]:

            str = f"{frel}({e[0]},{e[1]})"
            e.append(frel)
            e.append(str)
            return e

