# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models, connection

def querry(q, params=None):
    cursor = connection.cursor()
    cursor.execute(q, params)
    header = tuple(col_info[0] for col_info in cursor.description)
    
    result = []
    for entry in cursor.fetchall():
        result.append(dict(zip(header, entry)))
    return result


class DelegacaoManager(models.Manager):
    def Ranking(self):
        q = """
        select sigla, nome, ouro, prata, bronze from delegacao
        order by ouro, prata, bronze;
        """
        return querry(q)

    def List(self):
        return querry("select sigla, nome from delegacao;")

class Delegacao(models.Model):
    sigla = models.CharField(primary_key=True, max_length=3)
    nome = models.CharField(max_length=40)
    linguas = models.TextField()
    n_participantes = models.SmallIntegerField()
    ouro = models.SmallIntegerField()
    prata = models.SmallIntegerField()
    bronze = models.SmallIntegerField()

    objects = DelegacaoManager()

    class Meta:
        managed = False
        db_table = 'delegacao'

class AtletaManager(models.Manager):
    def Filtra(self, delegacao='', genero='', esporte=''):
        skipDeleg = 'true' if not delegacao else 'false'
        skipGenero = 'true' if not genero else 'false'
        skipEsporte = 'true' if not esporte else 'false'

        q = """
        select a.registro_olimp, a.genero, a.nome, a.delegacao,
        d.nome as delegacao_nome, e.nome as esporte from atleta a
        join delegacao d on d.sigla = a.delegacao
        join esporte e on e.codigo = a.esporte
        where
        (%s or delegacao = %s) and
        (%s or genero = %s) and
        (%s or esporte = %s)
        order by delegacao_nome, a.nome;
        """
        return querry(q, [skipDeleg, delegacao, skipGenero, genero, skipEsporte, esporte])

    def Info(self, id):
        q = """
        select a.*, d.nome as delegacao_nome,
        e.nome as esporte_nome from atleta a
        join esporte e on e.codigo = a.esporte
        join delegacao d on d.sigla = a.delegacao
        where a.registro_olimp = %s;
        """
        return querry(q, [id])

    def Medalhas(self, id):
        return (0, 0, 0)


class Atleta(models.Model):
    registro_olimp = models.CharField(primary_key=True, max_length=10)
    passaporte = models.CharField(max_length=10)
    nome = models.CharField(max_length=50)
    data_nasc = models.DateField()
    peso = models.DecimalField(max_digits=6, decimal_places=3)
    altura = models.DecimalField(max_digits=4, decimal_places=3)
    genero = models.CharField(max_length=1)
    inabilidades = models.TextField(blank=True, null=True)
    delegacao = models.ForeignKey('Delegacao', models.DO_NOTHING, db_column='delegacao')
    esporte = models.ForeignKey('Esporte', models.DO_NOTHING, db_column='esporte')

    objects = AtletaManager()
    class Meta:
        managed = False
        db_table = 'atleta'

class Local(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    nome_oficial = models.CharField(unique=True, max_length=50)
    apelido = models.CharField(max_length=30, blank=True, null=True)
    capacidade = models.IntegerField()
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=30)
    rua = models.CharField(max_length=40)
    numero = models.IntegerField(blank=True, null=True)
    referencia = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'local'

class EsporteManager(models.Manager):
    def List(self):
        return querry("select codigo, nome from esporte;")

class Esporte(models.Model):
    codigo = models.CharField(primary_key=True, max_length=3)
    nome = models.CharField(unique=True, max_length=15)
    ano_intro = models.SmallIntegerField(blank=True, null=True)

    objects = EsporteManager()
    class Meta:
        managed = False
        db_table = 'esporte'
