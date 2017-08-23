import mongoengine as me


class Evento(me.EmbeddedDocument):
	descricao = me.StringField()
	inicio = me.StringField()
	fim = me.StringField()
	pendente = me.StringField()

class Usuario(me.Document):
	nome = me.StringField()
	login = me.StringField()
	password = me.StringField()
	eventos = me.EmbeddedDocumentListField(Evento)
