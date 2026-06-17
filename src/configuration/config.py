import os
from dotenv import load_dotenv

load_dotenv()


class MySQLConfig:
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    USER = 'root'
    PASSWORD = '123456'
    DATABASE = 'edu'


class Neo4jConfig:
    URI = 'neo4j://localhost:7687'
    USER = 'neo4j'
    PASSWORD = '13629102205ddd'


class ServerConfig:
    HOST = '0.0.0.0'
    PORT = 8000


class ModelConfig:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    UIE_MODEL_PATH = os.path.join(BASE_DIR, 'uie_pytorch', 'uie_base_pytorch')


class DeepSeekConfig:
    API_KEY = os.getenv('DEEPSEEK_API_KEY')
    BASE_URL = 'https://api.deepseek.com'
    MODEL = 'deepseek-chat'

