import json
from bson.json_util import loads, dumps
from datetime import datetime

# **************************************************************************************
# 									Metodos dos USUARIOS
# **************************************************************************************
def get_usuarios(usuarios_model):
    try:
		#Retorna lista de usuarios no formato Json
        return usuarios_model.objects.to_json(), 200
    except:
        return 'Erro em get_usuarios', 404


def get_usuario(usuarios_model, id):
    try:
		#Retorna um usuario como o respectivo login
        usuario = usuarios_model.objects.get(login=id)
        return usuario.to_json(), 200
    except:
        return 'Erro get_usuario {}.'.format(id), 404


def create_usuario(usuario_model, data):
    try:
        new = {
            'nome': '',
            'login': '',
            'password': '',
            'eventos': []
        }
		
		#Atribuo cada um dos objetos filho para gerar o pai 
        for k in list(new.keys()):
            if k in data:
                new[k] = data[k]
		
        usuario = usuario_model(**new)
        usuario.save()
        return 'Usuário criado com sucesso!!', 201
    except:
        return 'Erro em criar usuário.', 400


def delete_usuario(usuario_model, id):
    try:
        usuario = usuario_model.objects.get(login=id)
        usuario.delete()
        return 'Usuário deletado.', 200
    except:
        return 'Erro em deletar usuário.', 400


def update_usuario(usuario_model, id, data):
    try:
        usuario = usuario_model.objects.get(login=id)
        if 'nome' in data:
            usuario.update(nome=data['nome'])
        if 'login' in data:
            usuario.update(login=data['login'])
        if 'password' in data:
            usuario.update(password=data['password'])
        if 'eventos' in data:
            usuario.update(eventos=data['eventos'])
        usuario.save()
        return 'Usuário atualizado.', 200
    except:
        return 'Erro em atualizar usuário', 400


# **************************************************************************************
# 									Metodos dos Eventos
# **************************************************************************************
def get_eventos(usuario_model, id):
    try:
        usuario = usuario_model.objects.get(login=id)
		#Crio um dicionario que vai me retornar a lista de eventos daquele usuario
        eventos = [dict(e.to_mongo()) for e in usuario.eventos]
		#Converto para formato json
        return json.dumps({'eventos': eventos})
    except Exception as e:
        return 'Erro em get_eventos '+str(e), 404


def get_evento(usuario_model, id, e_id):
    try:
		#Retorna um evento especifico do usuario
        usuario = usuario_model.objects.get(login=id)
        return usuario.eventos.get(descricao=e_id).to_json(), 200
    except:
        return 'Erro em get_evento {}'.format(e_id), 404


def create_evento(usuario_model, evento_model, id, data):
    try:
        new = {
            'descricao': '',				
            'inicio': '', 
            'fim': '', #datetime.now(),#strptime("01/01/17 09:00", "%d/%m/%y %H:%M"),
            'pendente' : 'false',				
        }
        for k in list(new.keys()):
        	if k in data:
        		new[k] = data[k]
        print(data['pendente'])
        #if 'descricao' in data:
        #    new['descricao']= data['descricao']
        #if 'data' in data:
        #    new['data']= data['data']
        #if 'inicio' in data:
        #    new['inicio'] = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
        #if 'fim' in data:
        #    new['fim'] = data['fim']#datetime.strptime(data['fim'], "%d-%m-%Y %H:%M:%S")
        #if 'pendente' in data:
        #    new['pendente'] = data['pendente']
        evento = evento_model(**new)
        usuario = usuario_model.objects.get(login=id)
		#Adiciona o evento na lista do usuario e salva no banco
        usuario.eventos.append(evento)
        usuario.save()
        return 'Evento adicionado', 201
    except Exception as e:
        return 'Erro em criar evento '+str(e), 400


def delete_evento(usuario_model, id, e_id):
    try:
        usuario = usuario_model.objects.get(login=id)
        usuario.eventos.filter(descricao=e_id).delete()
        usuario.save()
        return 'Evento deletado.', 200
    except:
        return 'Erro em deletar evento.', 400


def update_evento(usuario_model, id, e_id, data):
    try:
        usuario = usuario_model.objects.get(login=id)
        evento = usuario.eventos.get(descricao=e_id)

        if 'descricao' in data:
           evento.descricao = data['descricao']
        if 'inicio' in data:
           evento.inicio = data['inicio']
        if 'fim' in data:
           evento.fim = data['fim']
        if 'pendente' in data:
           evento.pendente = data['pendente']

        evento.save()
        return 'Evento atualizado', 200
    except Exception as e:
        return 'Erro em atualizar evento '+str(e), 400


def transform_output(s):
    return json.dumps(json.loads(s))
