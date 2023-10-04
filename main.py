from fastapi import FastAPI, HTTPException, status, Response
import uvicorn
import requests
from models import Time


app = FastAPI()

times = {}

url = 'https://api.api-futebol.com.br/v1/campeonatos/10/tabela'
headers = {
    'Authorization': f'Bearer live_170a3c7147b1b1a86220ce0924c9b7'
}

response = requests.get(url, headers=headers)

data = response.json()

#busca os dados referente a cada posição da tabela.
def buscar_dados():

    for position in range(20):
        time_data = data[position]

        pos = time_data['posicao']
        print(data)
        time = {
            'posicao': time_data['posicao'],
            'time': time_data['time']['nome_popular'],
            'pontos': time_data['pontos'],
            'vitorias': time_data['vitorias']
        }

        times[pos] = time 

    return times
        

buscar_dados()


@app.get('/times')
async def get_times():
    return times


@app.get('/times/{time_id}')
async def get_time(time_id: int):
    try:
        time = times[time_id]
        return time
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Time não encontrado')


@app.post('/times')
async def post_time(time: Time):
    last_key = sorted(times.keys())[-1]
    next_key = last_key + 1
    time.id = next_key
    times[next_key] = time
    return time 


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
