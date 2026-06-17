from src.configuration.config import *


def get_mysql_config():
    return MySQLConfig


def get_neo4j_config():
    return Neo4jConfig


def get_server_config():
    return ServerConfig


def get_model_config():
    return ModelConfig

def get_deepseek_config():
    return DeepSeekConfig
