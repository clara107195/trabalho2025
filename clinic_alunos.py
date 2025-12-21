import heapq
import random
import numpy as np
import json

# Parâmetros da aplicação
# ---
NUM_MEDICOS = 3
TAXA_CHEGADA = 10 / 60
TEMPO_MEDIO_CONSULTA = 15
TEMPO_SIMULACAO = 8 * 60
DISTRIBUICAO_TEMPO_CONSULTA = "exponential"

CHEGADA = "chegada"
SAIDA = "saída"

# --- Modelo para o evento
# Evento = (tempo: Float, tipo: String, doente: String)
# --- Funções de manipulação
def e_tempo(e):
    return e[0] #tempo de chegada

def e_tipo(e):
    return e[1] #tipo de consulta necessária

def e_doente(e):
    return e[2] #dados do paciente


# ---
# --- Modelo para a Queue de Eventos
# queueEventos = [Evento]
# --- Funções de manipulação
def procuraPosQueue(q, t): #procurar o indice onde inserir o evento
    i = 0
    while i < len(q) and t > q[i][0]:
        i = i + 1
    return i

def enqueue(q, e): #inserir evento na queue de eventos
    pos = procuraPosQueue(q, e[0])
    return q[:pos] + [e] + q[pos:]

def dequeue(q): #remover o evento mais próximo
    e = q[0]
    q = q[1:]
    return e, q

# --- Modelo para o médico
# Médico = [id: String, ocupado: Boolean, doente_corrente: String, total_tempo_ocupado: Float, inicio_ultima_consulta: Float]
# --- Funções de manipulação
def m_id(e): # retorna o id do médico
    return e[0]

def m_ocupado(e): # retorna se o médico está ocupado
    return e[1]

def mOcupa(m): # altera o estado de ocupado do médico
    m[1] = not m[1]
    return m

def m_doente_corrente(e): # retorna o doente corrente do médico
    return e[2]

def mDoenteCorrente(m, d): # altera o doente corrente do médico
    m[2] = d
    return m

def m_total_tempo_ocupado(e): # retorna o tempo total ocupado do médico
    return e[3]

def mTempoOcupado(m, t):  # altera o tempo total ocupado do médico
    m[3] = t
    return m

def m_inicio_ultima_consulta(e): # retorna o tempo de início da última consulta do médico
    return e[4]

def mInicioConsulta(m, t): # altera o tempo de início da última consulta do médico
    m[4] = t
    return m 
# ---

# --- Utilização das distribuições para gerar chegadas e durações das consultas
# ---
def gera_intervalo_tempo_chegada(lmbda):  
    return np.random.exponential(1 / lmbda) 

def gera_tempo_consulta():  
    if DISTRIBUICAO_TEMPO_CONSULTA == "exponential":
        return np.random.exponential(TEMPO_MEDIO_CONSULTA)
    elif DISTRIBUICAO_TEMPO_CONSULTA == "normal":
        return max(0, np.random.normal(TEMPO_MEDIO_CONSULTA, 5))
    elif DISTRIBUICAO_TEMPO_CONSULTA == "uniform":
        return np.random.uniform(TEMPO_MEDIO_CONSULTA * 0.5, TEMPO_MEDIO_CONSULTA * 1.5)

# --- Funções auxiliares
# -----------------------------------------
# --- Procura o primeiro médico livre
# ---
def procuraMedico(lista):
    res = None
    i = 0
    encontrado = False
    while not encontrado and i < len(lista):
        if not lista[i][1]:
            res = lista[i]
            encontrado = True
        i = i + 1
    return res

# -----------------------------------------

def simula():
    tempo_atual = 0.0
    contadorDoentes = 1
    queueEventos = [] # Lista de eventos que vão acontecer, ordenada por tempo de ocorrência do evento
    queue = [] # Fila de espera - doentes à espera de médico disponível
    # --- Geração da lista de médicos
    medicos = [[f"m{i}", False, None, 0.0, 0.0] for i in range(NUM_MEDICOS)]
    # ---
    # --- Geração das chegadas de doentes
    chegadas = {} # dicionário de suporte para a geração das consultas
    tempo_atual = tempo_atual + gera_intervalo_tempo_chegada(TAXA_CHEGADA)
    while tempo_atual < TEMPO_SIMULACAO:
        doente_id = "d" + str(contadorDoentes)
        contadorDoentes += 1
        chegadas[doente_id] = tempo_atual
        queueEventos = enqueue(queueEventos, (tempo_atual, CHEGADA, doente_id))
        tempo_atual = tempo_atual + gera_intervalo_tempo_chegada(TAXA_CHEGADA)
    # ---
    # ---
    # --- Tratamento dos eventos
    doentes_atendidos = 0

    while queueEventos != []:
        evento, queueEventos = dequeue(queueEventos)
        print(e_tipo(evento), evento)
        tempo_atual = e_tempo(evento)

        if e_tipo(evento) == CHEGADA:
            medico_livre = procuraMedico(medicos)
            if medico_livre:
                medico_livre = mOcupa(medico_livre) # o médico ficou ocupado
                medico_livre = mInicioConsulta(medico_livre, tempo_atual)
                tempo_consulta = gera_tempo_consulta()
                medico_livre = mDoenteCorrente(medico_livre, e_doente(evento)) # médico fica a atender o doente que acabou de chegar
                queueEventos = enqueue(queueEventos, (tempo_atual + tempo_consulta, SAIDA, e_doente(evento)))
            else:
                queue.append((evento[2], tempo_atual)) # doente fica à espera
                print(f"Fila de Espera({len(queue)}): ", queue)
        elif evento[1] == SAIDA:
            doentes_atendidos += 1
            # Vamos libertar o médico e despachar o doente
            i = 0
            encontrado = False
            while i < len(medicos) and not encontrado: # vou procurar o médico que está a atender o doente cuja consulta terminou
                if m_doente_corrente(medicos[i]) == e_doente(evento): # se encontrei o médico que está a atender o doente deste evento
                    medicos[i] = mOcupa(medicos[i]) # o médico ficou livre
                    medicos[i] = mDoenteCorrente(medicos[i], None)  # não está a atender nenhum doente
                    medicos[i] = mTempoOcupado(medicos[i], m_total_tempo_ocupado(medicos[i]) + tempo_atual - m_inicio_ultima_consulta(medicos[i])) # incremento o tempo da consulta que terminou
                    encontrado = True
                i = i + 1
            
            medico = medicos[i-1]

            if queue != []: # se há doentes à espera vou ocupar o médico que ficou livre...
                ev, queue = dequeue(queue)
                prox_doente, tchegada = ev
                medico = mOcupa(medico)
                medico = mInicioConsulta(medico, tempo_atual)
                medico = mDoenteCorrente(medico, prox_doente)
                tempo_consulta = gera_tempo_consulta()
                queueEventos = enqueue(queueEventos, (tempo_atual + tempo_consulta, SAIDA, prox_doente))

    print(f"Doentes atendidos: {doentes_atendidos}")

if __name__ == "__main__":
    simula()




# pessoas

def carrega_pessoas(ficheiro="pessoas.json"):
    with open(ficheiro, encoding="utf-8") as f:
        pessoas = json.load(f)
    return pessoas