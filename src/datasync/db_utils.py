import pymysql
from neo4j import GraphDatabase
from src.configuration.dependency import get_mysql_config, get_neo4j_config


def get_mysql_connection():
    cfg = get_mysql_config()
    conn = pymysql.connect(
        host=cfg.MYSQL_HOST,
        port=cfg.MYSQL_PORT,
        user=cfg.USER,
        password=cfg.PASSWORD,
        database=cfg.DATABASE,
        charset='utf8mb4'
    )
    return conn


def get_neo4j_driver():
    cfg = get_neo4j_config()
    driver = GraphDatabase.driver(
        uri=cfg.URI,
        auth=(cfg.USER, cfg.PASSWORD),
    )
    return driver


def query_mysql(sql: str):
    conn = get_mysql_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        conn.close()


def run_cypher(driver, query: str, params: dict = None):
    with driver.session() as session:
        result = session.run(query, parameters=params or {})
        return [record.data() for record in result]


