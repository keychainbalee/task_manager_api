from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, Generator
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# CONSTANT & CONFIGURATION DATABASE
# Alamat file database SQLite yang akan dibuat otomatis
DATABASE_URL = "sqlite:///./todos.db"

# Engine untuk menghubungkan kode dengan SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session untuk berinteraksi (tambah, baca, hapus) dengan database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class untuk membuat model tabel
Base = declarative_base()


# MODEL DATABASE (Tabel Asli di SQLite)
class TodoModel(Base):
    __tablename__ = "todos"  # Nama tabel di dalam database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task = Column(String, index=True)
    priority = Column(String)
    is_completed = Column(Boolean, default=False)


# Buat tabelnya secara otomatis 
Base.metadata.create_all(bind=engine)


# PYDANTIC SCHEMAS (Validasi Request/Response)
# Skema untuk menerima data baru
class TodoCreate(BaseModel):
    task: str
    priority: str
    is_completed: bool = False

# Skema untuk mengirim respon balik ke klien 
class TodoResponse(BaseModel):
    id: int
    task: str
    priority: str
    is_completed: bool

    class Config:
        from_attributes = True


# DEPENDENCY (Fungsi Penghubung Database)
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# INITIALIZATION FASTAPI
app = FastAPI(title="To-Do List API dengan SQLite")


# ENDPOINTS 

# GET ALL
@app.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoModel).all()
    return todos


# GET BY ID
@app.get("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def get_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tugas tidak ditemukan")
    return todo


# POST
@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(new_item: TodoCreate, db: Session = Depends(get_db)):
    # Ubah data dari Pydantic menjadi format Model Database
    db_todo = TodoModel(**new_item.model_dump())
    
    db.add(db_todo)      # Daftarkan data baru ke database
    db.commit()          # Simpan permanen
    db.refresh(db_todo)  # Ambil data terbaru (termasuk ID yang digenerate otomatis)
    return db_todo


# PUT
@app.put("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todo_total(todo_id: int, updated_item: TodoCreate, db: Session = Depends(get_db)):
    todo_query = db.query(TodoModel).filter(TodoModel.id == todo_id)
    todo = todo_query.first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tugas tidak ditemukan")
        
    todo_query.update(updated_item.model_dump(), synchronize_session=False)
    db.commit()
    return todo_query.first()


# PATCH
class TodoPatch(BaseModel):
    task: Optional[str] = None
    priority: Optional[str] = None
    is_completed: Optional[bool] = None

@app.patch("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todo_partial(todo_id: int, partial_data: TodoPatch, db: Session = Depends(get_db)):
    todo_query = db.query(TodoModel).filter(TodoModel.id == todo_id)
    todo = todo_query.first()
    
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tugas tidak ditemukan")
        
    # Ambil data yang dikirim saja
    incoming_data = partial_data.model_dump(exclude_unset=True)
    
    todo_query.update(incoming_data, synchronize_session=False)
    db.commit()
    return todo_query.first()


# DELETE
@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tugas tidak ditemukan")
        
    db.delete(todo)
    db.commit()
    return {"status": "success", "message": f"Tugas dengan ID {todo_id} berhasil dihapus"}