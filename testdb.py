from app import db
from app.models import *

tit = 'test title'
bod = 'test body'
for u in range(1,20):
    title = tit + str(u)
    body = bod + str(u)
    po = Post(title = title, body = body)
    db.session.add(po)
    db.session.commit()