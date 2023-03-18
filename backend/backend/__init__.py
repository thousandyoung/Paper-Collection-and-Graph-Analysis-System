from neomodel import config
# if neo4j is in docker, turn localhost into your docker ip 
# config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'
config.DATABASE_URL = 'bolt://neo4j:12345678@192.168.1.217:7687'