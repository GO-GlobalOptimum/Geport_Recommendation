from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import random
from dotenv import load_dotenv

def data_preprocessing():
    # Load environment variables from .env file
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 루트 디렉토리에 있는 .env 파일의 절대 경로
    env_path = os.path.join(current_dir, '..', '.env')

    # .env 파일 로드
    load_dotenv(dotenv_path=env_path)

    # 환경 변수에서 사용자와 주소 가져오기
    db_user = os.getenv("DB_USER")
    db_address = os.getenv("DB_ADDRESS")
    db_name = os.getenv("DB_NAME")

    print(db_user, db_address, db_name)

    # 데이터베이스 URL 설정 (비밀번호 생략)
    DB_URL = f'mysql+pymysql://{db_user}@{db_address}/{db_name}'
    engine = create_engine(DB_URL, pool_recycle=3600)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 데이터베이스 세션 생성
    db = SessionLocal()

    # member 테이블 데이터 조회
    members_result = db.execute(text("SELECT member_id, age, gender, mbti FROM member"))
    posts_result = db.execute(text("""
        SELECT post.post_id, post.is_public, post.is_comment, post.member_id, category_post.category_id AS category_id
        FROM post
        LEFT JOIN category_post ON post.post_id = category_post.post_id
    """))
    view_result = db.execute(text("SELECT member_id, post_id FROM view"))

    # 컬럼 이름 가져오기 (keys() 메서드 사용 후 리스트로 변환)
    member_columns = list(members_result.keys())
    post_columns = list(posts_result.keys())
    view_columns = list(view_result.keys())

    # 데이터 가져오기 (fetchall() 호출)
    members = members_result.fetchall()
    posts = posts_result.fetchall()
    views = view_result.fetchall()

    # 딕셔너리 형태로 변환
    member_dicts = [dict(zip(member_columns, member)) for member in members]
    post_dicts = [dict(zip(post_columns, post)) for post in posts]
    view_dicts = [dict(zip(view_columns, view)) for view in views]

    # 데이터 출력
    for member_dict in member_dicts:
        print(member_dict)
        print("-" * 20)

    for post_dict in post_dicts:
        print(post_dict)
        print("-" * 20)

    for view_dict in view_dicts:
        print(view_dict)
        print("-" * 20)

    # 세션 종료
    db.close()

    # ID 매핑 함수 정의
    def map_ids(members, posts, views, user_start_id=0, item_start_id=100000):
        member_id_map = {member['member_id']: user_start_id + i for i, member in enumerate(members)}
        post_id_map = {post['post_id']: item_start_id + i for i, post in enumerate(posts)}

        mapped_members = []
        for member in members:
            mapped_members.append({
                'member_id': member_id_map[member['member_id']],
                'age': member['age'],
                'gender': member['gender'],
                'mbti': member['mbti']
            })

        mapped_posts = []
        for post in posts:
            mapped_posts.append({
                'post_id': post_id_map[post['post_id']],
                'is_public': post['is_public'],
                'is_comment': post['is_comment'],
                'category_id': post['category_id'],
                'created_by': member_id_map[post['member_id']]
            })

        mapped_views = []
        for view in views:
            mapped_views.append({
                'member_id': member_id_map[view['member_id']],
                'post_id': post_id_map[view['post_id']]
            })

        return mapped_members, mapped_posts, mapped_views

    # 데이터 매핑
    mapped_members, mapped_posts, mapped_views = map_ids(member_dicts, post_dicts, view_dicts)


    relation_mapping = {}

    with open("datasets/relation_list.txt", "r") as f:
        for line in f:
            relation_name = line.strip().split()[0]
            relation_id = line.strip().split()[1]
            relation_mapping[relation_name] = relation_id

    # train_user_dict와 test_user_dict 생성
    train_user_dict = {}
    test_user_dict = {}

    for view in mapped_views:
        member_id = view['member_id']
        post_id = view['post_id']
        if member_id not in train_user_dict:
            train_user_dict[member_id] = []
        train_user_dict[member_id].append(post_id)

    for member_id, post_ids in train_user_dict.items():
        random.shuffle(post_ids)
        split_index = int(len(post_ids) * 0.8)
        train_user_dict[member_id] = post_ids[:split_index]
        test_user_dict[member_id] = post_ids[split_index:]

    # train.txt와 test.txt 파일 생성 함수 정의
    def create_train_test_files(train_user_dict, test_user_dict, filename_train='datasets/train.txt', filename_test='datasets/test.txt'):
        with open(filename_train, 'w') as f:
            for data in train_user_dict.items():
                member_id = data[0]
                post_ids = [post_id + 100000 for post_id in data[1]]  # post_id에 100000 더함
                f.write(f"{member_id} {' '.join(map(str, post_ids))}\n")
        
        with open(filename_test, 'w') as f:
            for data in test_user_dict.items():
                member_id = data[0]
                post_ids = [post_id + 100000 for post_id in data[1]]  # post_id에 100000 더함
                f.write(f"{member_id} {' '.join(map(str, post_ids))}\n")

    create_train_test_files(train_user_dict, test_user_dict)

    # kg_final.txt 파일 생성 함수 정의
    def create_kg_final(mapped_members, mapped_posts, relation_mapping, filename='datasets/kg_final.txt'):
        with open(filename, 'w') as f:
            # 사용자 부가정보
            for member in mapped_members:
                member_id = member['member_id']
                f.write(f"{member_id} {relation_mapping['age']} {member['age']}\n")
                f.write(f"{member_id} {relation_mapping['gender']} {member['gender']}\n")
                f.write(f"{member_id} {relation_mapping['mbti']} {member['mbti']}\n")
            
            # 게시물 부가정보
            for post in mapped_posts:
                post_id = post['post_id']
                f.write(f"{post_id} {relation_mapping['is_public']} {post['is_public']}\n")
                f.write(f"{post_id} {relation_mapping['is_comment']} {post['is_comment']}\n")
                try:
                    f.write(f"{post_id} {relation_mapping['category']} {post['category_id']}\n")
                except:
                    f.write(f"{post_id} 0 0\n")
                f.write(f"{post_id} {relation_mapping['created_by']} {post['created_by']}\n")

    create_kg_final(mapped_members, mapped_posts, relation_mapping)

    print("Data saved successfully.")