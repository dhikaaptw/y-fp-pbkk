from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import models, schemas, auth
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aplikasi Y API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def enrich_post(post, db, current_user=None):
    uid = current_user.id if current_user else -1
    is_liked = any(l.user_id == uid for l in post.likes)
    is_saved = any(s.user_id == uid for s in post.saves)
    return {
        "id": post.id, "content": post.content,
        "created_at": post.created_at, "updated_at": post.updated_at,
        "owner_id": post.owner_id, "owner": post.owner,
        "like_count": len(post.likes), "comment_count": len(post.comments),
        "save_count": len(post.saves), "is_liked": is_liked,
        "is_saved": is_saved, "comments": post.comments,
    }

@app.post("/auth/register", response_model=schemas.UserOut, status_code=201)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(400, "Email sudah terdaftar")
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        raise HTTPException(400, "Username sudah dipakai")
    user = models.User(username=user_data.username, email=user_data.email,
                       hashed_password=auth.hash_password(user_data.password))
    db.add(user); db.commit(); db.refresh(user)
    return user

@app.post("/auth/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(401, "Email atau password salah")
    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}

@app.get("/auth/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# post 

@app.get("/posts", response_model=List[schemas.PostOut])
def get_all_posts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db),
                  current_user: Optional[models.User] = Depends(auth.get_optional_user)):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()
    return [enrich_post(p, db, current_user) for p in posts]

@app.post("/posts", response_model=schemas.PostOut, status_code=201)
def create_post(post_data: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    if not post_data.content.strip():
        raise HTTPException(400, "Post tidak boleh kosong")
    if len(post_data.content) > 280:
        raise HTTPException(400, "Post maksimal 280 karakter")
    post = models.Post(content=post_data.content, owner_id=current_user.id)
    db.add(post); db.commit(); db.refresh(post)
    return enrich_post(post, db, current_user)

@app.put("/posts/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, post_data: schemas.PostUpdate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post: raise HTTPException(404, "Post tidak ditemukan")
    if post.owner_id != current_user.id: raise HTTPException(403, "Bukan post kamu")
    post.content = post_data.content
    db.commit(); db.refresh(post)
    return enrich_post(post, db, current_user)

@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post: raise HTTPException(404, "Post tidak ditemukan")
    if post.owner_id != current_user.id: raise HTTPException(403, "Bukan post kamu")
    db.delete(post); db.commit()

@app.get("/posts/search", response_model=List[schemas.PostOut])
def search_posts(username: str, db: Session = Depends(get_db),
                 current_user: Optional[models.User] = Depends(auth.get_optional_user)):
    posts = (db.query(models.Post).join(models.User)
             .filter(models.User.username.ilike(f"%{username}%"))
             .order_by(models.Post.created_at.desc()).all())
    return [enrich_post(p, db, current_user) for p in posts]

@app.get("/posts/saved", response_model=List[schemas.PostOut])
def get_saved_posts(db: Session = Depends(get_db),
                    current_user: models.User = Depends(auth.get_current_user)):
    saved_post_ids = [s.post_id for s in current_user.saves]
    posts = (db.query(models.Post).filter(models.Post.id.in_(saved_post_ids))
             .order_by(models.Post.created_at.desc()).all())
    return [enrich_post(p, db, current_user) for p in posts]

#like comment save follow
@app.post("/posts/{post_id}/like", response_model=schemas.LikeOut)
def toggle_like(post_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post: raise HTTPException(404, "Post tidak ditemukan")
    existing = db.query(models.Like).filter(
        models.Like.user_id == current_user.id, models.Like.post_id == post_id).first()
    if existing:
        db.delete(existing); db.commit(); db.refresh(post)
        return {"message": "Unlike", "is_liked": False, "like_count": len(post.likes)}
    else:
        db.add(models.Like(user_id=current_user.id, post_id=post_id))
        db.commit(); db.refresh(post)
        return {"message": "Like", "is_liked": True, "like_count": len(post.likes)}

@app.post("/posts/{post_id}/comments", response_model=schemas.CommentOut, status_code=201)
def add_comment(post_id: int, data: schemas.CommentCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post: raise HTTPException(404, "Post tidak ditemukan")
    if not data.content.strip(): raise HTTPException(400, "Komentar tidak boleh kosong")
    comment = models.Comment(content=data.content, post_id=post_id, owner_id=current_user.id)
    db.add(comment); db.commit(); db.refresh(comment)
    return comment

@app.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(auth.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment: raise HTTPException(404, "Komentar tidak ditemukan")
    if comment.owner_id != current_user.id: raise HTTPException(403, "Bukan komentar kamu")
    db.delete(comment); db.commit()

@app.post("/posts/{post_id}/save", response_model=schemas.SaveOut)
def toggle_save(post_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post: raise HTTPException(404, "Post tidak ditemukan")
    existing = db.query(models.Save).filter(
        models.Save.user_id == current_user.id, models.Save.post_id == post_id).first()
    if existing:
        db.delete(existing); db.commit()
        return {"message": "Post dihapus dari simpanan", "is_saved": False}
    else:
        db.add(models.Save(user_id=current_user.id, post_id=post_id))
        db.commit()
        return {"message": "Post disimpan", "is_saved": True}

@app.post("/users/{username}/follow", response_model=schemas.FollowOut)
def toggle_follow(username: str, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    target = db.query(models.User).filter(models.User.username == username).first()
    if not target: raise HTTPException(404, "User tidak ditemukan")
    if target.id == current_user.id: raise HTTPException(400, "Tidak bisa follow diri sendiri")
    existing = db.query(models.Follow).filter(
        models.Follow.follower_id == current_user.id,
        models.Follow.following_id == target.id).first()
    if existing:
        db.delete(existing); db.commit()
        return {"message": f"Unfollow @{username}", "is_following": False}
    else:
        db.add(models.Follow(follower_id=current_user.id, following_id=target.id))
        db.commit()
        return {"message": f"Follow @{username}", "is_following": True}