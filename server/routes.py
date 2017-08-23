from flask import render_template
import json
import time


def create_routes(blueprint, request, utils, models):
    api = blueprint('api', __name__)
	
	# ************************************************************************
	# Rotas de navegação
	# ************************************************************************
    @api.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @api.route('/cadastro', methods=['GET'])
    def cadastro():
        return render_template('cadastro.html')

    @api.route('/home', methods=['GET'])
    def home():
        return render_template('home.html')

    @api.route('/calendario', methods=['GET'])
    def calendario():
        return render_template('calendario.html')

    @api.route('/novo', methods=['GET'])
    def novo():
        return render_template('evento.html')


	# ************************************************************************
	# Rotas de API - comunicaçao com o mongo
	# ************************************************************************
    @api.route('/api/usuarios', methods=['GET', 'POST'])
    def usuarios_list_create():
        if request.method == 'GET':
            return utils.get_usuarios(models.Usuario)
        if request.method == 'POST':
            return utils.create_usuario(models.Usuario, request.get_json())

    @api.route('/api/usuarios/<string:id>', methods=['GET', 'PATCH', 'DELETE'])
    def usuarios_details(id):
        if request.method == 'GET':
            return utils.get_usuario(models.Usuario, id)
        if request.method == 'DELETE':
            return utils.delete_usuario(models.Usuario, id)
        if request.method == 'PATCH':
            return utils.update_usuario(models.Usuario, id, request.get_json())

    @api.route('/api/usuarios/<string:id>/eventos', methods=['GET', 'POST'])
    def eventos_list_create(id):
        if request.method == 'GET':
            return utils.get_eventos(models.Usuario, id)
        if request.method == 'POST':
            return utils.create_evento(models.Usuario, models.Evento, id, request.get_json())


    @api.route('/api/usuarios/<string:id>/eventos/<string:e_id>',
               methods=['GET','PATCH', 'DELETE'])
    def eventos_details(id, e_id):
        if request.method == 'GET':
            return utils.get_evento(models.Usuario, id, e_id)
        if request.method == 'DELETE':
            return utils.delete_evento(models.Usuario, id, e_id)
        if request.method == 'PATCH':
            return utils.update_evento(models.Usuario, id, e_id, request.get_json())

    return api
