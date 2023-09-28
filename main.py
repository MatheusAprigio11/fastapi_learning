from fastapi import FastAPI, HTTPException, status, Response
import uvicorn
import requests
import json
from models import Time


app = FastAPI()

times = {}

def buscar_dados():

    url = 'https://api.api-futebol.com.br/v1/campeonatos/10/tabela'
    headers = {
        'Authorization': f'Bearer live_170a3c7147b1b1a86220ce0924c9b7'
    }

    response = requests.get(url, headers=headers)

    data = response.json()
  # Dicionário para armazenar os detalhes de todos os times

    for p in range(20):
        time_data = data[p]

        nome_popular = time_data['time']['nome_popular']

        time = {
            'posicao': time_data['posicao'],
            'pontos': time_data['pontos'],
            'vitorias': time_data['vitorias']
        }

        times[nome_popular] = time  # Use o nome popular como chave

    return times
        

    print(response)





def minha_api(api):

   
    print(times)
    return times

buscar_dados()

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
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)









# if __name__ == '__main__':
#     buscar_dados()
#     