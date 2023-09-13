from fastapi import FastAPI, HTTPException, status, Response
import uvicorn

app = FastAPI()

cursos = {
    1: {
    "nome": "Python",
    "aulas": 20,
    "horas": 80,
    "instrutor": "Cleber"
    },
    2: {
    "nome": "Java",
    "aulas": 15,
    "horas": 60,
    "instrutor": "Leonardo"
    }
}

@app.get('/cursos')
async def get_cursos():
    return cursos

@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int):
    try:
        curso = cursos[curso_id]
        # curso.update({"id": curso_id})
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')


from models import Curso

@app.post('/cursos')
async def post_curso(curso: Curso):
    # last_key = - 1
    # # for k in cursos.keys():
    # #     last_key = k

    last_key = sorted(cursos.keys())[-1]
    next_key = last_key + 1
    curso.id = next_key
    cursos[next_key] = curso
    return curso

    # else:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Já existe um cruso com o ID {curso.id}")


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso):
    
    if curso_id in cursos:
        cursos[curso_id] = curso
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esse Curso não Existe.")
    
@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code= status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esse Curso não existe.")










if __name__ =='__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)