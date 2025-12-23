import json
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional
import datetime


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
    dados['medicos'].append(novo_medico)
    salvar_dados(arquivo, dados)

def adicionar_paciente_dados(novo_paciente, arquivo='pacientes.json'):
    """Adiciona um novo paciente ao arquivo de dados"""
    dados = carregar_dados(arquivo)
    dados['pacientes'].append(novo_paciente)
    salvar_dados(arquivo, dados)

def buscar_medico_por_id(id_medico, arquivo='medicos.json'):
    """Busca um médico pelo ID"""
    dados = carregar_dados(arquivo)
    medico = next((m for m in dados['medicos'] if m['id'] == id_medico), None)
    return medico, dados

def buscar_paciente_por_id(id_paciente, arquivo='pacientes.json'):
    """Busca um paciente pelo ID"""
    dados = carregar_dados(arquivo)
    paciente = next((p for p in dados['pacientes'] if p['id'] == id_paciente), None)
    return paciente, dados

def remover_medico_por_id(id_medico, arquivo='medicos.json'):
    """Remove um médico pelo ID"""
    dados = carregar_dados(arquivo)
    medico = next((m for m in dados['medicos'] if m['id'] == id_medico), None)
    if medico:
        dados['medicos'] = [m for m in dados['medicos'] if m['id'] != id_medico]
        salvar_dados(arquivo, dados)
        return True
    return False

def remover_paciente_por_id(id_paciente, arquivo='pacientes.json'):
    """Remove um paciente pelo ID"""
    dados = carregar_dados(arquivo)
    paciente = next((p for p in dados['pacientes'] if p['id'] == id_paciente), None)
    if paciente:
        dados['pacientes'] = [p for p in dados['pacientes'] if p['id'] != id_paciente]
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










