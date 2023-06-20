from py2neo import Graph,Node
from requests import get
graph = Graph("bolt://localhost:7687", auth=("neo4j", "moiz11..."))
def Create_user(uname,uemail,upass,ip_add,gender1):

    node1 = Node("Person", name=uname, email=uemail, password=upass, ip=ip_add,gender=gender1,lepisode="episode1")

    graph.create(node1)
    node2 = Node("episode",name="episode1",date="",chat="",email=uemail)


    graph.create(node2)
    graph.run("""match (n:Person{email:$uemail}),(b:episode{email:$uemail}) create (n)-[r:has]->(b) return r""",
              uemail=uemail)


def get_episode(email):
    user = graph.run("""MATCH(n:Person) where n.email  = $email return n.lepisode""", email=email).data()

    return user[0]["n.lepisode"]
def get_episodetime(email,episode):
    user=graph.run("""match(n:episode{email:$email,name:$episode}) return n.date  """,email=email,episode=episode).data()
    return user[0]["n.date"]



def get_name(email):
    user = graph.run("""MATCH(n:Person) where n.email  = $email return n.name""",email=email).data()

    return user[0]["n.name"]
def new_rel(uname1,uname2,frel):
    utype="SN"
    node1 = Node("Person", name=uname1,type=utype)

    graph.create(node1)
    node1 = Node("Person", name=uname2,type=utype)

    graph.create(node1)
    cypher_query = f"""
        MATCH (n:Person {{name: $uname1, type: $utype}}),
        (b:Person {{name: $uname2, type: $utype}})
        CREATE (n)-[r:`{frel}`]->(b)
        RETURN r
        """
    graph.run(cypher_query, uname1=uname1, uname2=uname2, utype=utype)

def rel(uname1,uname2,frel):
    utype = "SN"
    node1 = Node("Person", name=uname2, type=utype)
    graph.create(node1)
    cypher_query = f"""
            MATCH (n:Person {{email: $uname1}}),
            (b:Person {{name: $uname2, type: $utype}})
            CREATE (n)-[r:`{frel}`]->(b)
            RETURN r
            """

    graph.run(cypher_query, uname1=uname1, uname2=uname2, utype=utype)




def get_gender(email):
    user = graph.run("""MATCH(n:Person) where n.email  = $email return n.gender""",email=email).data()

    return user[0]["n.gender"]



def check_email(uemail):
    user = graph.run("""MATCH(n:Person) where n.email  = $uemail with COUNT(n)>0 as user_exists Return user_exists""",uemail=uemail).data()

    if user[0]["user_exists"]:
        return True
    else:
        return False
def get_pass(email):
    pass1 = graph.run("""MATCH(n:Person) where n.email  = $email Return n.password""", email=email).data()
    return pass1[0]["n.password"]

def get_ip(email):
    ip = graph.run("""MATCH(n:Person) where n.email  = $email Return n.ip""", email=email).data()
    return ip[0]["n.ip"]
def update_ip(email,ip):
    ip = graph.run("""Match(n:Person{email:$email})set n.ip = $ip return n.ip""",email=email,ip=ip).data()
    return ip[0]["n.ip"]

def update_time(email,date,episode):

    time = graph.run("""Match(n:episode{email:$email,name:$episode})set n.date = $date return n.date""",email=email,date=date,episode=episode).data()

def createnewepisode(uemail,curr_date,episode):
    num=int(episode.split("episode")[1])
    num+=1
    num=str(num)
    newname="episode"+num
    node2 = Node("episode", name=newname, date=curr_date, chat="", email=uemail)

    graph.create(node2)
    graph.run("""match (n:Person{email:$uemail}),(b:episode{email:$uemail,name:$newname}) create (n)-[r:has]->(b) return r""",
              uemail=uemail,newname=newname)
    ip = graph.run("""Match(n:Person{email:$uemail})set n.lepisode = $newname return n.lepisode""", uemail=uemail, newname=newname).data()



def getchat(email):

    episode=get_episode(email)
    oldchat=graph.run("""MATCH(n:episode) where n.email  = $email and n.name=$episode return n.chat""",email=email,episode=episode).data()
    return oldchat[0]['n.chat']

def storechat(email,chat):
    episode = get_episode(email)
    oldchat=graph.run("""MATCH(n:episode) where n.email  = $email and n.name=$episode return n.chat""",email=email,episode=episode).data()



    chat=oldchat[0]['n.chat']+chat

    chat = graph.run("""Match(n:episode{email:$email,name:$episode})set n.chat = $chat return n.chat""",email=email,chat=chat,episode=episode).data()

def update_pass(email,password):

    pass1 = graph.run("""Match(n:Person{email:$email})set n.password = $password return n.password""",email=email,password=password).data()

