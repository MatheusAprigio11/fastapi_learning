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

def buscar_dados():

    url = 'https://api.api-futebol.com.br/v1/campeonatos/10/tabela'
    headers = {
        'Authorization': f'Bearer live_170a3c7147b1b1a86220ce0924c9b7'
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    posicoes = []
    
    for p in range(20):
        posicoes.append(data[p])
    
    for time in posicoes:
        times = {
            time: {
            "posicao": time,
            "time": time['time']['nome_popular'],
            "pontos": time['pontos'],
            "vitorias": time['vitorias']
            },
        }
        print(times.json())

    print(response)
    print(data[13]['time']['nome_popular'])
    print(data[13]['pontos'])
    


if __name__ =='__main__':
    buscar_dados()
    # uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)









# if __name__ == '__main__':
#     buscar_dados()
#     