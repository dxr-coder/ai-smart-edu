QUERY_NEO4J_TOOL = {
    "type": "function",
    "function": {
        "name": "query_neo4j",
        "description": "执行 Cypher 查询语句并返回结果",
        "parameters": {
            "type": "object",
            "properties": {
                "cypher": {
                    "type": "string",
                    "description": "要执行的 Cypher 查询语句"
                }
            },
            "required": ["cypher"]
        }
    }
}
