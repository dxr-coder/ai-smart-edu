from configuration.dependency import get_model_config
from uie_pytorch.uie_predictor import UIEPredictor
from src.datasync.db_utils import query_mysql
import os


def extract(texts: list[str], task_path: str = None, device: str = 'gpu'):
    if task_path is None:
        task_path = get_model_config().UIE_MODEL_PATH
    predictor = UIEPredictor(model=get_model_config().UIE_MODEL_PATH, task_path=task_path, device=device,
                             schema='知识点')
    result = predictor.predict(texts)
    return result


def extract_from_courses(task_path: str = None, prob_threshold: float = 0.3):
    rows = query_mysql('select id,course_name,course_introduce from course_info')
    results = []
    for row in rows:
        id = row[0]
        course_name = row[1]
        course_introduce = row[2] if row[2] is not None else row[1]
        result = extract([course_introduce], task_path=task_path)
        points = []
        for item in result[0].get("知识点", []):
            if item["probability"] > prob_threshold:
                points.append({"name": item["text"], "probability": float(item["probability"])})
        res = {"course_id": id, "course_name": course_name,
               "knowledge_points": points}
        results.append(res)
    return results


def extract_from_chapters(task_path: str = None, prob_threshold: float = 0.3):
    rows = query_mysql('select id,chapter_name,course_id from chapter_info')
    results = []
    for row in rows:
        chapter_id = row[0]
        chapter_name = row[1]
        course_id = row[2]
        result = extract([chapter_name], task_path=task_path)
        points = []
        for item in result[0].get("知识点", []):
            if item["probability"] > prob_threshold:
                points.append({"name": item["text"], "probability": float(item["probability"])})
        res = {"chapter_id": chapter_id, "chapter_name": chapter_name,
               "course_id": course_id, "knowledge_points": points}
        results.append(res)
    return results


def extract_from_questions(task_path: str = None, prob_threshold: float = 0.3):
    rows = query_mysql('select id,question_txt,course_id from test_question_info')
    results = []
    for row in rows:
        question_id = row[0]
        question_txt = row[1] if row[1] is not None else ''
        course_id = row[2]
        result = extract([question_txt], task_path=task_path)
        points = []
        for item in result[0].get("知识点", []):
            if item["probability"] > prob_threshold:
                points.append({"name": item["text"], "probability": float(item["probability"])})
        res = {"question_id": question_id, "question_txt": question_txt,
               "course_id": course_id, "knowledge_points": points}
        results.append(res)
    return results



