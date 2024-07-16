from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
import uvicorn

from DB import database
from ROUTERS import user, todo
from AUTH import athentication

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

db_dependency = Depends(database.get_db)

app.include_router(user.router)
app.include_router(athentication.router)
app.include_router(todo.router)

@app.get('/')
def start():
    return 'this is todo project!!'
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
'''
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")
'''
