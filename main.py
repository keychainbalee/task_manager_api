from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="To-Do List API v2")

# Simulasi Database menggunakan List of Dictionary
todo_db = [
    {"id": 1, "task": "Belajar routing FastAPI", "priority": "High", "is_completed": False},
    {"id": 2, "task": "Beli kopi untuk ngoding", "priority": "Medium", "is_completed": True}
]

# Skema utama untuk validasi data yang masuk
class TodoItem(BaseModel):
    id: int
    task: str
    priority: str  # Contoh: High, Medium, Low
    is_completed: bool = False
    
# GET ALL: Melihat semua tugas
@app.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todos():
    return {"status": "success", "data": todo_db}

# GET BY ID: Melihat satu tugas spesifik
@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def get_todo_by_id(todo_id: int):
    for item in todo_db:
        if item["id"] == todo_id:
            return {"status": "success", "data": item}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tugas tidak ditemukan")

# POST: Menambahkan tugas baru
@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(new_item: TodoItem):
    # Validasi: Pastikan ID tidak duplikat
    for item in todo_db:
        if item["id"] == new_item.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID sudah ada")
    
    # Masukkan ke database simulasi
    todo_db.append(new_item.model_dump())
    return {"status": "success", "message": "Tugas berhasil ditambahkan", "data": new_item}

# PUT: Mengupdate seluruh data tugas
@app.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def update_todo_total(todo_id: int, updated_item: TodoItem):
    for index, item in enumerate(todo_db):
        if item["id"] == todo_id:
            # Timpa data lama dengan data baru yang dikirim klien
            todo_db[index] = updated_item.model_dump()
            todo_db[index]["id"] = todo_id  # Mengunci agar ID tetap sama dengan URL
            return {"status": "success", "message": "Tugas berhasil diperbarui secara total"}
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tugas tidak ditemukan")

# Skema khusus PATCH (semua field opsional)
class TodoPatch(BaseModel):
    task: Optional[str] = None
    priority: Optional[str] = None
    is_completed: Optional[bool] = None

# PATCH: Mengubah status atau sebagian data tugas
@app.patch("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def update_todo_partial(todo_id: int, partial_data: TodoPatch):
    for index, item in enumerate(todo_db):
        if item["id"] == todo_id:
            current_item = todo_db[index]
            
            # Ambil data yang dikirim saja (abaikan yang bernilai None)
            incoming_data = partial_data.model_dump(exclude_unset=True)
            
            # Perbarui field yang dikirim saja
            current_item.update(incoming_data)
            
            todo_db[index] = current_item
            return {"status": "success", "message": "Sebagian data tugas berhasil diubah", "data": current_item}
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tugas tidak ditemukan")

# DELETE: Menghapus tugas
@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(todo_id: int):
    for index, item in enumerate(todo_db):
        if item["id"] == todo_id:
            todo_db.pop(index)
            return {"status": "success", "message": f"Tugas dengan ID {todo_id} berhasil dihapus"}
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tugas tidak ditemukan")