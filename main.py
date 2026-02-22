import random
import time
import numpy as np
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from sqlalchemy import ForeignKey, create_engine, select, func
engine = create_engine("sqlite:///mydb.db")
sess = sessionmaker(bind = engine)

class Base(DeclarativeBase):
 ...

class User(Base):
 __tablename__ = "user_table"
 id:Mapped[int] = mapped_column(primary_key=True)
 username:Mapped[str]

class Video(Base):
 __tablename__ = "video_table"
 id:Mapped[int] = mapped_column(primary_key=True)
 name:Mapped[str]

class Likes(Base):

 __tablename__ = "video_users_table"
 user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id"),primary_key=True)
 video_id:Mapped[int] = mapped_column(ForeignKey("video_table.id"),primary_key=True)
 like:Mapped[int] = mapped_column(default=1)



# [1,1,1,1] # 1 user
# [] # 2 user
# [] # 3 user
# from sqlalchemy import select
#
# session = get_session()
# session:Session
# session.execute(select(f))
def get_matrix():
  with sess() as session:
   likes = session.scalars(select(Likes))
   count_users = session.execute(select(func.count(User.id))).scalar()
   count_video = session.execute(select(func.count(Video.id))).scalar()
   matrix = np.zeros((count_users, count_video), dtype=np.int8)
   for i in likes:
    matrix[i.user_id-1][i.video_id-1] = i.like
   return matrix

class Recomendations:
 def cosine_similarity(self,A, B):
    # Числитель: скалярное произведение A и B
    dot_product = np.dot(A, B)
    # Знаменатель: произведение норм (длин) векторов
    norm_a = np.linalg.norm(A)
    norm_b = np.linalg.norm(B)

    if norm_a == 0 or norm_b == 0:
        return 0
    return dot_product / (norm_a * norm_b)

 def recommend(self,matrix, target_idx, n):
     target_user = matrix[target_idx]
     similarities = []


     for i, other_user in enumerate(matrix):
         if i == target_idx:
             continue

         # Применяем формулу с картинки
         sim = self.cosine_similarity(target_user, other_user)
         similarities.append((i, sim))

     # Находим самого похожего (максимальный косинус)
     best_match_idx, _ = max(similarities, key=lambda x: x[1])
     sims = sorted(similarities, key= lambda x: x[1], reverse=True)
     # Ищем видео, которое похожий юзер лайкнул (1), а наш еще не видел (0)
     recommendations = set()
     for sim in sims:
      for idx, rating in enumerate(matrix[sim[0]]):
          if target_user[idx] == 0 and rating == 1:
              recommendations.add(idx)
      if len(recommendations) >= n:
        return recommendations
     return recommendations

