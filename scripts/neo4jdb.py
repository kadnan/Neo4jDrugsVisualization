from neo4j import GraphDatabase


def delete_all(session):
    session.run('match (n) DETACH delete n')


def create_relationship(start_type, end_type, start_name, end_name, session, label='USED_BY'):
    q = "MATCH (a:{}),(b:{}) WHERE a.name = $start_name and b.name = $end_name CREATE (a)-[r:{}]->(b) RETURN type(r)".format(
        start_type, end_type, label)
    session.run(q, start_name=start_name, end_name=end_name)


def create_node(name, type, session):
    # Sending a parameterized query
    q = "create(n:{}{{name:$name}})".format(type, name)
    session.run(q, name=name)


def get_neo_connection(user, pwd):
    uri = "bolt://127.0.0.1:7687"
    driver = GraphDatabase.driver(uri, auth=(user, pwd))
    return driver
