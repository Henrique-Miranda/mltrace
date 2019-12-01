# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect
import datetime, time
import json
from lib.meli import Meli
from decouple import config

APP_ID = config('APP_ID')

CLIENT_SECRET = config('CLIENT_SECRET')

AUTH_URI = config('AUTH_URI')

meli = Meli(client_id=APP_ID, client_secret=CLIENT_SECRET)

app = Flask(__name__)

users = {'Henrique': [1, 5, 9], 'Jony': [2, 6, 10], 'Thiago': [3, 7, 11], 'Samuel': [4, 8, 12]}

@app.route('/gatoflix')
def hello_world():
    data = datetime.datetime.now().date()
    now = f'{data.day}/{data.month}/{data.year}'
    #lastdate = f'{data.day}/{data.month}/2019'

    currentuser = ''
    for u in users.keys():
        if data.month in users[u]: currentuser = u

    usr = list(users.keys())
    nextuser = ''
    try:
        nextuser = usr[usr.index(currentuser) + 1]
    except:
        nextuser = usr[0]

    lastuser = usr[usr.index(currentuser) - 1]

    dados = {'currentuser': currentuser, 'lastuser': lastuser, 'nextuser': nextuser, 'now': now}

    return render_template("home.html", dados=dados)

@app.route('/authorize')
def authorize():
    meli.authorize(request.args.get('code'), AUTH_URI)
    return """<div align='center'><h1>Cole o ID do anúncio abaixo Ex.: MLB-1128663825</h1><form class="" action="/post" method="get">
      <label for="anuncio">ID Anúncio</label><br>
      <input type="text" name="anuncio" id="anuncio" required="required"><br>
      <label for="valor">Valor</label><br>
      <input type="number" min="1" step="any" name="valor" id="valor" required="required"><br>
      <button type="submit" name="button">Postar anúncio</button><br>
    </form></div>"""

@app.route('/')
def login():
    if meli.access_token:
        return '<div align="center">Peça autorização para acessar o Clonador de Anúncios.</div>'
        #return redirect('https://auth.mercadolivre.com.br/authorization?client_id=2359959178558309&response_type=code&redirect_uri=https%3A%2F%2Fhenrique.pythonanywhere.com%2Fauthorize')
    else:
        return f"""<div align='center'><h1>MLTRACE</h1><br><h2>Importador de Anúncios</h2><a href='{meli.auth_url(redirect_URI=AUTH_URI)}'>Login</a></div>"""


@app.route('/get')
def getItem():
    idCode = request.args.get('code').replace('-', '')
    res = meli.get("/items/"+idCode, {'access_token':meli.access_token})
    data = json.loads(res.content)
    return data

@app.route('/post')
def postItem():
    idCode = request.args.get('anuncio').replace('-', '')
    valor = request.args.get('valor')
    valor = float(valor.replace(',', '.') if ',' in valor else valor)
    res = meli.get(f'/items/{idCode}')
    data = json.loads(res.content)
    temp = []
    for i in data['variations']:
        i['available_quantity'] = 2
        del i['catalog_product_id']
        i['price'] = valor
        temp.append(i)
    data['variations'] = temp
    j2 = {'title': data['title'], 'category_id': data['category_id'], 'price': valor, 'currency_id': data['currency_id'], 'available_quantity': data['available_quantity'], 'buying_mode': data['buying_mode'], 'listing_type_id': data['listing_type_id'], 'condition': data['condition'], 'description': data['descriptions'][0], 'video_id': data['video_id'], 'tags': data['tags'], 'warranty': data['warranty'], 'pictures': data['pictures'], 'variations': data['variations'], 'attributes': data['attributes'], 'accepts_mercadopago': data['accepts_mercadopago'], 'shipping': data['shipping'], 'sale_terms': data['sale_terms']}
    res = meli.post("/items", j2, {'access_token':meli.access_token})
    if res.status_code in (201, 200):
        return f"<div align='center'><br><h1>Pronto!</h1><br><h2>O produto {data['title']} de valor {valor}, já foi publicado na sua conta do ML.</h2><br><a href='{meli.auth_url(redirect_URI=AUTH_URI)}'>Postar outro</a><br></div>"
    return f"<div align='center'><br><h1>Ops! Erro {str(res.status_code)}</h1><br><h2>Algo deu errado tente novamente.</h2><br><a href='{meli.auth_url(redirect_URI=AUTH_URI)}'>Tentar de novo</a><br></div>"

@app.route('/calcml')
def calcml():
    return render_template('calcml.html')
 
