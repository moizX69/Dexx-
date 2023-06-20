from py2neo import Graph,Node
from website import database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "moiz11..."))
episode="episode1"
email="ahmadbilal@gmail.com"
episode=database.get_episode(email)
oldchat=graph.run("""MATCH(n:episode) where n.email  = $email and n.name=$episode return n.chat""",email=email,episode=episode).data()
print(oldchat)