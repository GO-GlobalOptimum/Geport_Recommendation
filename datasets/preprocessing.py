# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker, Session
# import os
# from dotenv import load_dotenv

# load_dotenv()
# DB_URL = f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_ADDRESS")}/{os.getenv("DB_NAME")}'
# engine = create_engine(DB_URL, pool_recycle=3600)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # 데이터베이스 세션 생성
# db = SessionLocal()

# # member 테이블 데이터 조회
# members_result = db.execute(text("SELECT * FROM member"))
# posts_result = db.execute(text("SELECT * FROM post"))
# post_tags = db.execute(text("SELECT * FROM post_tag"))

# # 컬럼 이름 가져오기 (keys() 메서드 사용 후 리스트로 변환)
# member_columns = list(members_result.keys())
# post_columns = list(posts_result.keys())
# post_tag_columns = list(post_tags.keys())

# # 데이터 가져오기 (fetchall() 호출)
# members = members_result.fetchall()
# posts = posts_result.fetchall()

# # 딕셔너리 형태로 변환
# member_dicts = [dict(zip(member_columns, member)) for member in members]
# post_dicts = [dict(zip(post_columns, post)) for post in posts]
# tag_dicts = [dict(zip(post_tag_columns, post_tag)) for post_tag in post_tags]

# # # 데이터 출력
# # for member_dict in member_dicts:
# #     print(member_dict)
# #     print("-" * 20)

# # for post_dict in post_dicts:
# #     print(post_dict)
# #     print("-" * 20)

# for tag_dict in tag_dicts:
#     print(tag_dict)
#     print("-" * 20)

# # 세션 종료
# db.close()


# # kg_final.txt에 저장