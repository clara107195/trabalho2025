import json
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional
import datetime
import re
import unicodedata



PRIORIDADE_MAP = {
    "emergência": 0,
    "alta": 1,
    "média": 2,
    "normal": 2,
    "baixa": 3
}

TIME_SLOTS = ["08:00-09:00","09:00-10:00","10:00-11:00","11:00-12:00",
              "14:00-15:00","15:00-16:00","16:00-17:00"]



import json
import os

def carregar_dados(arquivo):
    """Carrega dados do arquivo JSON"""
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {"medicos": []} if "medicos" in arquivo else {"pacientes": []}

def salvar_dados(arquivo, dados):
    """Salva dados no arquivo JSON"""
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def criar_medico(id_medico, nome, especialidade, disponivel):
    """Cria um novo médico com os dados fornecidos"""
    novo_medico = {
        "id": id_medico,
        "nome": nome,
        "ocupado": not disponivel,
        "doente_corrente": None,
        "especialidade": especialidade,
        "total_tempo_ocupado": 0.0,
        "inicio_ultima_consulta": 0.0
    }
    return novo_medico

def atualizar_medico(medico, nome, especialidade, disponivel):
    """Atualiza os dados de um médico existente"""
    medico['nome'] = nome
    medico['especialidade'] = especialidade
    medico['ocupado'] = not disponivel
    return medico

def criar_paciente(id_paciente, nome, idade, sexo, doenca, prioridade, fumador, alcool, atividade, cronico):
    """Cria um novo paciente com os dados fornecidos"""
    novo_paciente = {
        "id": id_paciente,
        "nome": nome,
        "idade": idade,
        "sexo": sexo,
        "doenca": doenca,
        "prioridade": prioridade,
        "atributos": {
            "fumador": fumador,
            "consome_alcool": alcool,
            "atividade_fisica": atividade,
            "cronico": cronico
        }
    }
    return novo_paciente

def atualizar_paciente(paciente, nome, idade, sexo, doenca, prioridade, fumador, alcool, atividade, cronico):
    """Atualiza os dados de um paciente existente"""
    paciente['nome'] = nome
    paciente['idade'] = idade
    paciente['sexo'] = sexo
    paciente['doenca'] = doenca
    paciente['prioridade'] = prioridade
    paciente['atributos']['fumador'] = fumador
    paciente['atributos']['consome_alcool'] = alcool
    paciente['atributos']['atividade_fisica'] = atividade
    paciente['atributos']['cronico'] = cronico
    return paciente

def adicionar_medico_dados(novo_medico, arquivo='medicos.json'):
    """Adiciona um novo médico ao arquivo de dados"""
    dados = carregar_dados(arquivo)
    if not isinstance(dados, dict):
        dados = {'medicos': []}
    if 'medicos' not in dados or not isinstance(dados['medicos'], list):
        dados['medicos'] = []
    dados['medicos'].append(novo_medico)
    salvar_dados(arquivo, dados)

def adicionar_paciente_dados(novo_paciente, arquivo='pacientes.json'):
    """Adiciona um novo paciente ao arquivo de dados"""
    dados = carregar_dados(arquivo)
    if not isinstance(dados, dict):
        dados = {'pacientes': []}
    if 'pacientes' not in dados or not isinstance(dados['pacientes'], list):
        dados['pacientes'] = []
    dados['pacientes'].append(novo_paciente)
    salvar_dados(arquivo, dados)



def procurar_medico_dados(chave):
    dados = carregar_dados('medicos.json')
    medicos = dados.get('medicos', [])

    chave = chave.lower()
    encontrados = []

    for medico in medicos:
        if str(medico.get('id')) == chave:
            return medico, dados

        nome = medico.get('nome', '').lower().replace('dr.', '').replace('dra.', '')

        if chave in nome:
            encontrados.append(medico)

    if len(encontrados) == 1:
        return encontrados[0], dados

    if len(encontrados) > 1:
        return encontrados, dados

    return None, dados





def procurar_paciente_dados(chave, arquivo='pacientes.json'):
    

    dados = carregar_dados(arquivo)
    pacientes = dados.get('pacientes') if isinstance(dados, dict) else []
    if not isinstance(pacientes, list):
        pacientes = []

    def normalizar(s):
        if not isinstance(s, str):
            return ''

        s = s.lower()
        s = unicodedata.normalize('NFKD', s)
        s = ''.join(c for c in s if not unicodedata.combining(c))
        s = re.sub(r'[^a-z\s]', '', s)
        s = re.sub(r'\s+', ' ', s).strip()
        return s

    chave_str = str(chave).strip()
    chave_norm = normalizar(chave)

    encontrados = []

    for paciente in pacientes:
        # 🔹 Buscar por ID (exato)
        if str(paciente.get('id')) == chave_str:
            return paciente, dados

        # 🔹 Buscar por nome (parcial)
        nome_norm = normalizar(paciente.get('nome', ''))
        if chave_norm and chave_norm in nome_norm:
            encontrados.append(paciente)

    if len(encontrados) == 1:
        return encontrados[0], dados

    if len(encontrados) > 1:
        return encontrados, dados

    return None, dados



def remover_medico_dados(chave, arquivo='medicos.json'):
    

    dados = carregar_dados(arquivo)
    medicos = dados.get('medicos') if isinstance(dados, dict) else []
    if not isinstance(medicos, list):
        medicos = []

    def normalizar(s):
        if not isinstance(s, str):
            return ''

        s = s.lower()
        s = re.sub(r'\bdr\.?\b|\bdra\.?\b', '', s)
        s = unicodedata.normalize('NFKD', s)
        s = ''.join(c for c in s if not unicodedata.combining(c))
        s = re.sub(r'[^a-z\s]', '', s)
        s = re.sub(r'\s+', ' ', s).strip()
        return s

    chave_str = str(chave).strip()
    chave_norm = normalizar(chave)

    encontrados = []

    for medico in medicos:
        # 🔹 ID (exato)
        if str(medico.get('id')) == chave_str:
            dados['medicos'] = [m for m in medicos if m.get('id') != medico.get('id')]
            salvar_dados(arquivo, dados)
            return True

        # 🔹 Nome (parcial)
        nome_norm = normalizar(medico.get('nome', ''))
        if chave_norm and chave_norm in nome_norm:
            encontrados.append(medico)

    # ⚠ Vários médicos com o mesmo nome
    if len(encontrados) > 1:
        return encontrados

    # 🔹 Apenas um encontrado pelo nome
    if len(encontrados) == 1:
        medico = encontrados[0]
        dados['medicos'] = [m for m in medicos if m.get('id') != medico.get('id')]
        salvar_dados(arquivo, dados)
        return True

    return False


def remover_paciente_dados(chave, arquivo='pacientes.json'):

    dados = carregar_dados(arquivo)
    pacientes = dados.get('pacientes') if isinstance(dados, dict) else []
    if not isinstance(pacientes, list):
        pacientes = []

    def normalizar(s):
        if not isinstance(s, str):
            return ''

        s = s.lower()
        s = unicodedata.normalize('NFKD', s)
        s = ''.join(c for c in s if not unicodedata.combining(c))
        s = re.sub(r'[^a-z\s]', '', s)
        s = re.sub(r'\s+', ' ', s).strip()
        return s

    chave_str = str(chave).strip()
    chave_norm = normalizar(chave)

    encontrados = []

    for paciente in pacientes:
        # 🔹 ID (exato)
        if str(paciente.get('id')) == chave_str:
            dados['pacientes'] = [p for p in pacientes if p.get('id') != paciente.get('id')]
            salvar_dados(arquivo, dados)
            return True

        # 🔹 Nome (parcial)
        nome_norm = normalizar(paciente.get('nome', ''))
        if chave_norm and chave_norm in nome_norm:
            encontrados.append(paciente)

    # ⚠ Vários pacientes com o mesmo nome
    if len(encontrados) > 1:
        return encontrados

    # 🔹 Apenas um encontrado pelo nome
    if len(encontrados) == 1:
        paciente = encontrados[0]
        dados['pacientes'] = [p for p in pacientes if p.get('id') != paciente.get('id')]
        salvar_dados(arquivo, dados)
        return True

    return False


def validar_campos_medico(id_medico, nome, especialidade):
    """Valida se todos os campos obrigatórios do médico estão preenchidos"""
    if not id_medico or not nome or not especialidade:
        return False
    return True

def validar_campos_paciente(id_paciente, nome, idade, sexo, doenca, prioridade, atividade):
    """Valida se todos os campos obrigatórios do paciente estão preenchidos"""
    if not all([id_paciente, nome, idade, sexo, doenca, prioridade, atividade]):
        return False
    return True

def validar_idade(idade_str):
    """Valida e converte a idade para inteiro"""
    if idade_str.isdigit():
        return int(idade_str), True
    return None, False


def validar_estrutura_medicos(dados):
    """Valida a estrutura esperada para o ficheiro de médicos.
    Espera um dict com chave 'medicos' -> list de objetos com pelo menos
    as chaves: 'id', 'nome', 'especialidade'."""
    if not isinstance(dados, dict):
        return False
    medicos = dados.get('medicos')
    if not isinstance(medicos, list):
        return False
    for m in medicos:
        if not isinstance(m, dict):
            return False
        if 'id' not in m or 'nome' not in m or 'especialidade' not in m:
            return False
        # opcional: tipos básicos
        if not isinstance(m.get('id'), (str, int)):
            return False
        if not isinstance(m.get('nome'), str) or not isinstance(m.get('especialidade'), str):
            return False
    return True


def validar_estrutura_pacientes(dados):
    """Valida a estrutura esperada para o ficheiro de pacientes.
    Espera um dict com chave 'pacientes' -> list de objetos com pelo menos
    as chaves: 'id', 'nome', 'idade', 'sexo', 'doenca', 'prioridade', 'atributos'."""
    if not isinstance(dados, dict):
        return False
    pacientes = dados.get('pacientes')
    if not isinstance(pacientes, list):
        return False
    for p in pacientes:
        if not isinstance(p, dict):
            return False
        required = ['id', 'nome', 'idade', 'sexo', 'doenca', 'prioridade', 'atributos']
        for k in required:
            if k not in p:
                return False
        if not isinstance(p.get('id'), (str, int)):
            return False
        if not isinstance(p.get('nome'), str):
            return False
        # idade deve ser numérico
        if not isinstance(p.get('idade'), int):
            return False
        if not isinstance(p.get('sexo'), str) or not isinstance(p.get('doenca'), str) or not isinstance(p.get('prioridade'), str):
            return False
        atr = p.get('atributos')
        if not isinstance(atr, dict):
            return False
        # atributos esperados
        if 'fumador' not in atr or 'consome_alcool' not in atr or 'atividade_fisica' not in atr or 'cronico' not in atr:
            return False
    return True





#Ordena os paciente por ordem de prioridade

def prioridade_para_num(p):
    return PRIORIDADE_MAP.get(p.lower(), 2)

#gerar tempos de chegada poison

def gera_intervalo_chegada(lmbda):
    return np.random.exponential(1.0 / lmbda)


#gera o tempo  de consulta

def gera_tempo_consulta(media, dist="exponential"):
    if dist == "exponential":
        return np.random.exponential(media)
    if dist == "normal":
        return max(0.1, np.random.normal(media, 5))
    if dist == "uniform":
        return np.random.uniform(media*0.5, media*1.5)
    return media


#insere eventos mantendo a ordenaçao

def enqueue_event(queue, evento):
    t = evento[0]
    i = 0
    while i < len(queue) and t > queue[i][0]:
        i += 1
    queue.insert(i, evento)


#estatisticas simples

def estatisticas(valores):
    if not valores:
        return {"media": 0, "max": 0, "min": 0}
    return {
        "media": sum(valores)/len(valores),
        "max": max(valores),
        "min": min(valores)
    }



def plot_fila(times, sizes):
    plt.figure(figsize=(8,4))
    plt.plot(times, sizes)
    plt.xlabel("Tempo (min)")
    plt.ylabel("Tamanho da fila")
    plt.grid(True)
    plt.show()

def plot_ocupacao(ocupacoes):
    plt.figure(figsize=(6,4))
    plt.bar(range(len(ocupacoes)), ocupacoes)
    plt.ylim(0,1)
    plt.show()

def plot_hist_tempo_espera(esperas):
    plt.figure(figsize=(6,4))
    plt.hist(esperas, bins=30)
    plt.xlabel("Tempo de Espera (min)")
    plt.show()










