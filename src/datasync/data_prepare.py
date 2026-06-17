from src.datasync.db_utils import query_mysql, get_neo4j_driver
from src.entity_extraction.extractor import extract_from_courses, extract_from_chapters, extract_from_questions

task_path = '../../finetuned/checkpoint/model_best'


def sync_categories():
    '''从mysql同步分类到neo4j'''
    rows = query_mysql('SELECT id,category_name FROM base_category_info')
    driver = get_neo4j_driver()

    for row in rows:
        category_id = row[0]
        name = row[1]
        cypher = '''
        MERGE (:分类 {category_id: $category_id, name: $name})  
        '''
        driver.execute_query(cypher, category_id=category_id, name=name)
    driver.close()
    print(f'同步了{len(rows)}个分类')


def sync_subjects():
    '''从mysql同步学科到neo4j'''
    rows = query_mysql('SELECT id,subject_name,category_id FROM base_subject_info')
    driver = get_neo4j_driver()
    for row in rows:
        subject_id = row[0]
        name = row[1]
        category_id = row[2]
        cypher = '''
        MATCH (c:分类 {category_id: $category_id}) 
        MERGE (s:学科 {subject_id: $subject_id, name: $name})
        MERGE (s)-[:BELONG]->(c)
        '''
        driver.execute_query(cypher, subject_id=subject_id, name=name, category_id=category_id)
    driver.close()
    print(f'同步了{len(rows)}个学科')


def sync_courses():
    rows = query_mysql('SELECT id,course_name,subject_id FROM course_info')
    driver = get_neo4j_driver()
    for row in rows:
        course_id = row[0]
        name = row[1]
        subject_id = row[2]
        cypher = '''
        MATCH (s:学科 {subject_id: $subject_id})
        MERGE (c:课程 {course_id: $course_id, name: $name})
        MERGE (c)-[:BELONG]->(s)
        '''
        driver.execute_query(cypher, subject_id=subject_id, course_id=course_id, name=name)
    driver.close()
    print(f'同步了{len(rows)}个课程')


def sync_chapters():
    rows = query_mysql('SELECT id,chapter_name,course_id FROM chapter_info')
    driver = get_neo4j_driver()
    for row in rows:
        chapter_id = row[0]
        name = row[1]
        course_id = row[2]
        cypher = '''
        MATCH (c:课程 {course_id: $course_id})
        MERGE (s:章节 {chapter_id: $chapter_id, name: $name})
        MERGE (s)-[:BELONG]->(c)
        '''
        driver.execute_query(cypher, course_id=course_id, chapter_id=chapter_id, name=name)
    driver.close()
    print(f'同步了{len(rows)}个章节')


def sync_videos():
    rows = query_mysql('SELECT id,video_name,chapter_id FROM video_info')
    driver = get_neo4j_driver()
    for row in rows:
        video_id = row[0]
        name = row[1]
        chapter_id = row[2]
        cypher = '''
        MATCH (c:章节 {chapter_id: $chapter_id})
        MERGE (v:视频 {video_id: $video_id, name: $name})
        MERGE (v)-[:BELONG]->(c)
        '''
        driver.execute_query(cypher, video_id=video_id, chapter_id=chapter_id, name=name)
    driver.close()
    print(f'同步了{len(rows)}个视频')


def sync_paper():
    rows = query_mysql('SELECT id,paper_title,course_id FROM test_paper')
    driver = get_neo4j_driver()
    for row in rows:
        paper_id = row[0]
        name = row[1]
        course_id = row[2]
        cypher = '''
        MATCH (c:课程 {course_id : $course_id })
        MERGE (p:试卷 {paper_id: $paper_id, name: $name})
        MERGE (p)-[:BELONG]->(c)
        '''
        driver.execute_query(cypher, paper_id=paper_id, course_id=course_id, name=name)
    driver.close()
    print(f'同步了{len(rows)}个试卷')


def sync_question():
    rows = query_mysql(
        'SELECT tp.paper_id, tp.question_id, tq.question_txt FROM test_paper_question tp, test_question_info tq WHERE tp.question_id = tq.id')
    driver = get_neo4j_driver()
    for row in rows:
        paper_id = row[0]
        name = row[2]
        question_id = row[1]
        cypher = '''
        MATCH (p:试卷 {paper_id : $paper_id })
        MERGE (q:试题 {question_id: $question_id, name: $name})
        MERGE (q)-[:BELONG]->(p)
        '''
        driver.execute_query(cypher, paper_id=paper_id, question_id=question_id, name=name)
    driver.close()
    print(f'同步了{len(rows)}个试题')


def sync_teachers():
    rows = query_mysql('SELECT id, teacher FROM course_info')
    driver = get_neo4j_driver()

    for row in rows:
        course_id = row[0]
        teacher_name = row[1]
        cypher = """
            MATCH (c:课程 {course_id: $course_id})
            MERGE (t:教师 {name: $teacher_name})
            MERGE (c)-[:HAVE]->(t)
        """
        driver.execute_query(cypher, course_id=course_id, teacher_name=teacher_name)
    driver.close()
    print(f'同步了 {len(rows)} 门课程的教师信息')


def sync_prices():
    rows = query_mysql('SELECT id,actual_price  FROM course_info')
    driver = get_neo4j_driver()

    for row in rows:
        course_id = row[0]
        price = float(row[1] if row[1] is not None else 0)
        cypher = """
            MATCH (c:课程 {course_id: $course_id})
            MERGE (p:价格 {price: $price})
            MERGE (c)-[:HAVE]->(p)
        """
        driver.execute_query(cypher, course_id=course_id, price=price)
    driver.close()
    print(f'同步了 {len(rows)} 门课程的价格信息')


def sync_users():
    rows = query_mysql('SELECT id,birthday,gender  FROM user_info')
    driver = get_neo4j_driver()

    for row in rows:
        user_id = row[0]
        birthday = row[1]
        gender = row[2] if row[2] is not None else ''
        cypher = """
            MERGE (:学生 {user_id: $user_id, birthday: $birthday, gender: $gender})
        """
        driver.execute_query(cypher, user_id=user_id, birthday=birthday, gender=gender)
    driver.close()
    print(f'同步了 {len(rows)} 个学生的信息')


def sync_favors():
    rows = query_mysql('SELECT user_id,course_id,create_time FROM favor_info')
    driver = get_neo4j_driver()
    for row in rows:
        user_id = row[0]
        course_id = row[1]
        create_time = row[2]
        cypher = """
        MATCH (u:学生{user_id: $user_id})
        MATCH (c:课程{course_id: $course_id})
        MERGE (u)-[:FAVOR{时间:$create_time}]->(c)
        """
        driver.execute_query(cypher, user_id=user_id, course_id=course_id, create_time=create_time)
    driver.close()
    print(f'同步了 {len(rows)} 个收藏信息')


def sync_watches():
    rows = query_mysql('SELECT user_id,chapter_id,position_sec,update_time FROM user_chapter_progress')
    driver = get_neo4j_driver()
    for row in rows:
        user_id = row[0]
        chapter_id = row[1]
        position_sec = row[2]
        update_time = str(row[3]) if row[3] is not None else ''
        cypher = """
        MATCH (u:学生{user_id: $user_id})
        MATCH (c:章节{chapter_id: $chapter_id})
        MERGE (u)-[:WATCH{进度: $position_sec, 最后观看时间: $update_time}]->(c)
        """
        driver.execute_query(cypher, user_id=user_id, chapter_id=chapter_id, position_sec=position_sec,
                             update_time=update_time)
    driver.close()
    print(f'同步了 {len(rows)} 个观看信息')


def sync_answers():
    rows = query_mysql('SELECT user_id,question_id,is_correct FROM test_exam_question')
    driver = get_neo4j_driver()
    for row in rows:
        user_id = row[0]
        question_id = row[1]
        is_correct = row[2]
        cypher = """
        MATCH (u:学生{user_id: $user_id})
        MATCH (q:试题{question_id: $question_id})
        MERGE (u)-[:ANSWER{是否正确: $is_correct}]->(q)
        """
        driver.execute_query(cypher, user_id=user_id, question_id=question_id, is_correct=is_correct)
    driver.close()
    print(f'同步了 {len(rows)} 个答题记录')


def sync_knowledge_points():
    driver = get_neo4j_driver()
    courses = extract_from_courses(task_path=task_path)
    for course in courses:
        for point in course['knowledge_points']:
            name = point['name']
            cypher = '''
                MATCH (c:课程 {course_id: $course_id})
                MERGE (kp:知识点 {name: $name})
                MERGE (c)-[:HAVE]->(kp)
                '''
            driver.execute_query(cypher, name=name, course_id=course['course_id'])
    chapters = extract_from_chapters(task_path=task_path)
    for chapter in chapters:
        for point in chapter['knowledge_points']:
            name = point['name']
            cypher = '''
                MATCH (c:章节 {chapter_id: $chapter_id})
                MERGE (kp:知识点 {name: $name})
                MERGE (c)-[:HAVE]->(kp)
                '''
            driver.execute_query(cypher, name=name, chapter_id=chapter['chapter_id'])

    questions = extract_from_questions(task_path=task_path)
    for question in questions:
        for point in question['knowledge_points']:
            name = point['name']
            cypher = '''
                MATCH (q:试题 {question_id: $question_id})
                MERGE (kp:知识点 {name: $name})
                MERGE (q)-[:HAVE]->(kp)
                '''
            driver.execute_query(cypher, name=name, question_id=question['question_id'])
    driver.close()


def sync_knowledge_related():
    driver = get_neo4j_driver()
    cypher = """
    MATCH (c:章节)-[:HAVE]->(kp:知识点)
    RETURN c.chapter_id, COLLECT(kp.name) AS kps
    """
    res = driver.execute_query(cypher)
    for record in res.records:
        kps = record['kps']
        if len(kps) >= 2:
            for i in range(len(kps)):
                for j in range(i + 1, len(kps)):
                    cypher = """
                     MATCH (a:知识点 {name: $name1}), (b:知识点 {name: $name2})
                     MERGE (a)-[:RELATED]->(b)
                    """
                    driver.execute_query(cypher, name1=kps[i], name2=kps[j])
    cypher = """
        MATCH (c:试卷)-[:HAVE]->(kp:知识点)
        RETURN c.paper_id, COLLECT(kp.name) AS kps
        """
    res = driver.execute_query(cypher)
    for record in res.records:
        kps = record['kps']
        if len(kps) >= 2:
            for i in range(len(kps)):
                for j in range(i + 1, len(kps)):
                    cypher = """
                         MATCH (a:知识点 {name: $name1}), (b:知识点 {name: $name2})
                         MERGE (a)-[:RELATED]->(b)
                        """
                    driver.execute_query(cypher, name1=kps[i], name2=kps[j])
    driver.close()


def sync_knowledge_belong():
    driver = get_neo4j_driver()

    # 查出每门课的知识点名
    rows = driver.execute_query('''
        MATCH (c:课程)-[:HAVE]->(kp:知识点)
        RETURN c.course_id AS course_id, kp.name AS name
    ''')

    # 查对应章节的知识点，匹配了就建 BELONG
    for record in rows.records:
        course_id = record['course_id']
        course_kp_name = record['name']

        chapters = driver.execute_query('''
            MATCH (c:课程 {course_id: $course_id})<-[:BELONG]-(ch:章节)
            WHERE ch.name CONTAINS $kp_name
            MATCH (ch)-[:HAVE]->(ch_kp:知识点)
            RETURN ch_kp.name
        ''', course_id=course_id, kp_name=course_kp_name)

        for ch_record in chapters.records:
            ch_kp_name = ch_record['ch_kp.name']
            driver.execute_query('''
                MATCH (a:知识点 {name: $ch_name}), (b:知识点 {name: $course_kp_name})
                MERGE (a)-[:BELONG]->(b)
            ''', ch_name=ch_kp_name, course_kp_name=course_kp_name)

    driver.close()


def sync_knowledge_need():
    driver = get_neo4j_driver()

    # 查出所有课程及其章节（按 chapter_id 排序）
    rows = driver.execute_query('''
        MATCH (c:课程)<-[:BELONG]-(ch:章节)
        RETURN c.course_id AS course_id, ch.chapter_id AS chapter_id, ch.name AS chapter_name
        ORDER BY c.course_id, ch.chapter_id
    ''')

    # 按课程分组，同一门课的章节排好序
    current_course = None
    chapters = []
    for record in rows.records:
        course_id = record['course_id']
        chapter_id = record['chapter_id']

        if course_id != current_course:
            # 处理上一门课的章节配对
            if len(chapters) >= 2:
                for i in range(len(chapters) - 1):
                    prev_ch = chapters[i]
                    next_ch = chapters[i + 1]
                    # 前一章的知识点被后一章的知识点 NEED
                    driver.execute_query('''
                        MATCH (prev:章节 {chapter_id: $prev_id})-[:HAVE]->(kp_prev:知识点)
                        MATCH (next:章节 {chapter_id: $next_id})-[:HAVE]->(kp_next:知识点)
                        MERGE (kp_next)-[:NEED]->(kp_prev)
                    ''', prev_id=prev_ch, next_id=next_ch)
            current_course = course_id
            chapters = [chapter_id]
        else:
            chapters.append(chapter_id)

    # 处理最后一门课
    if len(chapters) >= 2:
        for i in range(len(chapters) - 1):
            prev_ch = chapters[i]
            next_ch = chapters[i + 1]
            driver.execute_query('''
                MATCH (prev:章节 {chapter_id: $prev_id})-[:HAVE]->(kp_prev:知识点)
                MATCH (next:章节 {chapter_id: $next_id})-[:HAVE]->(kp_next:知识点)
                WHERE kp_prev.name <> kp_next.name
                MERGE (kp_next)-[:NEED]->(kp_prev)
            ''', prev_id=prev_ch, next_id=next_ch)

    driver.close()


if __name__ == '__main__':
    # 数据同步（按依赖顺序）
    # sync_categories()      # 分类
    # sync_subjects()        # 学科
    # sync_courses()         # 课程
    # sync_chapters()        # 章节
    # sync_videos()          # 视频
    # sync_paper()           # 试卷
    # sync_question()        # 试题
    # sync_teachers()        # 教师
    # sync_prices()          # 价格
    # sync_users()           # 学生
    # sync_favors()          # 收藏
    # sync_watches()         # 观看
    # sync_answers()         # 答题

    # 知识图谱
    # sync_knowledge_points()    # 抽取知识点 → Neo4j（耗时较长）
    # sync_knowledge_related()   # 知识点相关关系
    # sync_knowledge_belong()    # 知识点包含关系
    # sync_knowledge_need()      # 知识点先修关系

    print("请在代码中选择要执行的同步函数，取消注释即可运行")
