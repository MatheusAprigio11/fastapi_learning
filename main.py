from fastapi import FastAPI, HTTPException, status, Response
import uvicorn
import requests
import json


app = FastAPI()

times = {
    1: {
    "time": "São Paulo",
    "pontos": 28,
    "posicao": 13,
    "vitorias": 7
    },
    2: {
    "time": "Botafogo",
    "pontos": 51,
    "posicao": 1,
    "vitorias": 16
    }
}

@app.get('/times')
async def get_times():
    return times

@app.get('/times/{time_id}')
async def get_time(time_id: int):
    try:
        time = times[time_id]
        # curso.update({"id": curso_id})
        return time
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Time não encontrado')


from models import Time

@app.post('/times')
async def post_time(time: Time):
    # last_key = - 1
    # # for k in cursos.keys():
    # #     last_key = k

    last_key = sorted(times.keys())[-1]
    next_key = last_key + 1
    time.id = next_key
    times[next_key] = time
    return time 

    # else:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Já existe um cruso com o ID {curso.id}")


@app.put('/times/{time_id}')
async def put_time(time_id: int, time: Time):
    
    if time_id in times:
        times[time_id] = time
        return time
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esse time não Existe.")
    
@app.delete('/times/{time_id}')
async def delete_time(time_id: int):
    if time_id in times:
        del times[time_id]
        return Response(status_code= status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esse time não existe.")


if __name__ =='__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)







# def buscar_dados():
#     request = requests.get("http://localhost:3002/api/todo")
#     todos = json.loads(request.content)
#     print(todos)
#     print(todos[0]['titulo'])

# if __name__ == '__main__':
#     buscar_dados()
#     https://www.treinaweb.com.br/blog/consumindo-apis-com-python-parte-1#:~:text=Conclus%C3%A3o,ser%C3%A1%20utilizado%20para%20esta%20requisi%C3%A7%C3%A3o.