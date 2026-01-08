import FreeSimpleGUI as sg
from funcoes import *

escuro='#2196f3'
claro='#c3e3fd'



# Layout do menu principal
layout = [
    [sg.Text('Sistema de Gestão Clínica', background_color=claro, text_color=escuro,
             font=('Helvetica', 20, 'bold'), justification='center', expand_x=True)],

    
    [sg.Text(background_color=claro, size=(1,2))],

    
    [sg.Text('', background_color=claro, size=(8,1)), sg.Button('Simulação Clínica', button_color=(claro, escuro), size=(32, 4), font=('Helvetica', 12), key='-SIMULACAO-'), sg.Text('', background_color=claro, size=(10,2))],
    [sg.Text('', background_color=claro, size=(8,1)), sg.Button('Alterar Dados', button_color=(claro, escuro), size=(32, 4), font=('Helvetica', 12), key='-ALTERAR-'), sg.Text('', background_color=claro, size=(10,2))],
    [sg.Text('', background_color=claro, size=(8,1)), sg.Button('Importar Dados', button_color=(claro, escuro), size=(32, 4), font=('Helvetica', 12), key='-IMPORTAR-'), sg.Text('', background_color=claro, size=(10,2))],
    
    [sg.Text(background_color=claro, size=(0,0))],

    
    [sg.Text('', background_color=claro, size=(6,1)), sg.Button('Sair', size=(12, 1), font=('Helvetica', 11), key='-SAIR-', button_color=('white', 'red'), pad=(0,20)), sg.Text('', background_color=claro, size=(10,1))]
]


def popup_sim_nao(message, title=None, background_color=None, text_color=None):
   
    bg = background_color if background_color is not None else claro
    txt = text_color if text_color is not None else escuro
    btn_layout = [[sg.Text(message, background_color=bg, text_color=txt)], [sg.Text('', background_color=bg, size=(3,1)), sg.Button('Sim', button_color=(claro, escuro)), sg.Text('', background_color=bg, size=(1,1)), sg.Button('Não', button_color=(claro, escuro)), sg.Text('', background_color=bg, size=(3,1))]]
    win = sg.Window(title or '', btn_layout, modal=True, background_color=bg)
    event, values = win.read()
    win.close()
    if event is None:
        return 'Não'
    return event



def popup_ok(message, title=None, background_color=None, button_color=None, text_color=None):
    
    bg = background_color if background_color is not None else claro
    txt = text_color if text_color is not None else escuro
    btn_col = button_color if button_color is not None else (claro, escuro)
    layout = [[sg.Text(message, background_color=bg, text_color=txt, pad=(10,10))], [ sg.Button('OK', button_color=btn_col), sg.Text('', background_color=bg, size=(6,1))]]
    w = sg.Window(title or '', layout, modal=True, background_color=bg)
    e, v = w.read()
    w.close()
    return e


def verificar_dados_importados():
    """
    Verifica se existem dados válidos de médicos ou pacientes importados.
    Retorna (tem_medicos, tem_pacientes)
    """
    import os
    
    # Verificar se os ficheiros existem
    if not os.path.exists('medicos.json') or not os.path.exists('pacientes.json'):
        return False, False
    
    # Carregar dados
    dados_medicos = carregar_dados('medicos.json')
    dados_pacientes = carregar_dados('pacientes.json')
    
    # Verificar médicos
    tem_medicos = False
    if isinstance(dados_medicos, dict) and 'medicos' in dados_medicos:
        medicos_lista = dados_medicos['medicos']
        if isinstance(medicos_lista, list) and len(medicos_lista) > 0:
            tem_medicos = True
    
    # Verificar pacientes
    tem_pacientes = False
    if isinstance(dados_pacientes, dict) and 'pacientes' in dados_pacientes:
        pacientes_lista = dados_pacientes['pacientes']
        if isinstance(pacientes_lista, list) and len(pacientes_lista) > 0:
            tem_pacientes = True
    
    return tem_medicos, tem_pacientes


def importar_dados():
    
    caminho_medicos = sg.popup_get_file(
    'Escolha o ficheiro de médicos',
    file_types=(('JSON Files', '*.json'),),
    initial_folder='.',
    save_as=False, background_color=claro, text_color=escuro, button_color=(claro, escuro)
    )

    if not caminho_medicos:
        return

    
    caminho_pacientes = sg.popup_get_file(
    'Escolha o ficheiro de pacientes',
    file_types=(('JSON Files', '*.json'),),
    initial_folder='.',
    save_as=False, background_color=claro, text_color=escuro, button_color=(claro, escuro)
    )

    if not caminho_pacientes:
        return

    dados_medicos = carregar_dados(caminho_medicos)
    dados_pacientes = carregar_dados(caminho_pacientes)

   
    if not isinstance(dados_medicos, dict) or 'medicos' not in dados_medicos:
        sg.popup('Ficheiro de médicos inválido!', title='Erro', background_color=claro, text_color=escuro)
        return

    if not isinstance(dados_pacientes, dict) or 'pacientes' not in dados_pacientes:
        sg.popup('Ficheiro de pacientes inválido!', title='Erro', background_color=claro, text_color=escuro)
        return

    # guardar como base oficial da aplicação
    salvar_dados('medicos.json', dados_medicos)
    salvar_dados('pacientes.json', dados_pacientes)

    sg.popup('Dados importados com sucesso!', title='Sucesso',background_color=claro,text_color=escuro)
    

def alterar_dados():
    
    
    tem_medicos, tem_pacientes = verificar_dados_importados()
    
    if not tem_medicos and not tem_pacientes:
        sg.popup('Não há dados na base. Importe médicos ou pacientes antes de alterar.', 
                title='Aviso', background_color=claro, text_color=escuro)
        return
    

    coluna_medicos = [
        [sg.Text('Gestão de Médicos', font=('Helvetica', 14, 'bold'), justification='center', background_color=claro, text_color=escuro,expand_x=True, pad=(0,15))],
        [sg.Button('Adicionar Médico', size=(25, 2), key='-ADD-MEDICO-', button_color=(claro, escuro), pad=(0,10),font=('Helvetica', 11))],
        [sg.Button('Editar Médico', size=(25, 2), key='-EDIT-MEDICO-', button_color=(claro, escuro), pad=(0,10),font=('Helvetica', 11))],
        [sg.Button('Remover Médico', size=(25, 2), key='-REM-MEDICO-', button_color=(claro,escuro), pad=(0,10),font=('Helvetica', 11))],
        [sg.Button('Listar Médicos', size=(25, 2), key='-LIST-MEDICOS-', button_color=(claro, escuro), pad=(0,10),font=('Helvetica', 11))]
    ]
    
    
    coluna_pacientes = [
        [sg.Text('Gestão de Pacientes', font=('Helvetica', 14, 'bold'), justification='center', background_color=claro, text_color=escuro,expand_x=True, pad=(0,15))],
        [sg.Button('Adicionar Paciente', size=(25, 2), key='-ADD-PACIENTE-', button_color=(claro, escuro), pad=(0,10),font=('Helvetica', 11))],
        [sg.Button('Editar Paciente', size=(25, 2), key='-EDIT-PACIENTE-', button_color=(claro, escuro), pad=(0,10),font=('Helvetica', 11))],
        [sg.Button('Remover Paciente', size=(25, 2), key='-REM-PACIENTE-', button_color=('white', 'dark red'), pad=(0,10),font=('Helvetica', 11))],
        [sg.Button('Listar Pacientes', size=(25, 2), key='-LIST-PACIENTES-', button_color=(claro, escuro), pad=(0,10),font=('Helvetica', 11))]
    ]
    
    
    layout = [
        [sg.Text('Alteração de Dados', font=('Helvetica', 18, 'bold'), justification='center', expand_x=True, background_color=claro, text_color=escuro,pad=(0,20))],
        
        [sg.Column(coluna_medicos, element_justification='center', vertical_alignment='top', background_color=claro,expand_x=True), 
         sg.VerticalSeparator(pad=(20,0)),
         sg.Column(coluna_pacientes, element_justification='center', vertical_alignment='top', background_color=claro,expand_x=True)],
        [sg.Push(background_color=claro),
        sg.Button('Voltar ao Menu', size=(18, 1), key='-VOLTAR-', button_color=(claro, escuro), pad=(0,10), font=('Helvetica', 10)),
        sg.Push(background_color=claro)]
    ]
    
    window = sg.Window('Alteração de Dados', layout, size=(750, 500), element_justification='center', background_color=claro,finalize=True)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, '-VOLTAR-'):
            window.close()
            return
        
        if event == '-ADD-MEDICO-':
            adicionar_medico()
        
        elif event == '-EDIT-MEDICO-':
            editar_medico()
        
        elif event == '-REM-MEDICO-':
            remover_medico()
        
        elif event == '-ADD-PACIENTE-':
            adicionar_paciente()
        
        elif event == '-EDIT-PACIENTE-':
            editar_paciente()
        
        elif event == '-REM-PACIENTE-':
            remover_paciente()
        
        elif event == '-LIST-MEDICOS-':
            listar_medicos()

        elif event == '-LIST-PACIENTES-':
            listar_pacientes()



def adicionar_medico():

    dados = carregar_dados('medicos.json')
    medicos = dados.get('medicos') if isinstance(dados, dict) else None
    if not medicos:
        sg.popup('Não há médicos registados!', title='Aviso', background_color=claro, text_color=escuro)
        return
    
    layout_add = [
        [sg.Text('Adicionar Novo Médico', font=('Helvetica', 14, 'bold'),background_color=claro,text_color=escuro)],
        [sg.Text('ID:',background_color=claro,text_color=escuro), sg.Input(key='-ID-', size=(30, 1),background_color=claro,text_color=escuro)],
        [sg.Text('Nome:',background_color=claro,text_color=escuro), sg.Input(key='-NOME-', size=(30, 1),background_color=claro,text_color=escuro)],
        [sg.Text('Especialidade:',background_color=claro,text_color=escuro), sg.Input(key='-ESPECIALIDADE-', size=(30, 1),background_color=claro,text_color=escuro)],
        [sg.Text('Disponível:',background_color=claro,text_color=escuro), sg.Combo(['Sim', 'Não'], default_value='Sim', key='-DISPONIVEL-', readonly=True,background_color=claro,text_color=escuro)],
        [sg.Button('Guardar', key='-GUARDAR-',button_color=(claro, escuro)), sg.Button('Cancelar', key='-CANCELAR-',button_color=(claro, escuro))],
    
    ]
    
    window = sg.Window('Adicionar Médico', layout_add, modal=True,background_color=claro)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return
        
        if event == '-GUARDAR-':
            if not validar_campos_medico(values['-ID-'], values['-NOME-'], values['-ESPECIALIDADE-']):
                sg.popup('Por favor, preencha todos os campos necessários!', title='Erro', background_color=claro, text_color=escuro)
            else:
                disponivel = values['-DISPONIVEL-'] == 'Sim'
                novo_medico = criar_medico(values['-ID-'], values['-NOME-'], values['-ESPECIALIDADE-'], disponivel)
                adicionar_medico_dados(novo_medico)
                sg.popup('Médico adicionado com sucesso!', title='Médico Adicionado', background_color=claro, text_color=escuro)
                window.close()
                return


def editar_medico():
    
    dados = carregar_dados('medicos.json')
    medicos = dados.get('medicos') if isinstance(dados, dict) else None
    if not medicos:
        sg.popup('Não há médicos registados!', title='Aviso', background_color=claro, text_color=escuro)
        return
    
    escolha = sg.popup_get_text('Digite o ID do médico que pretende editar:', title='Selecionar Médico',background_color=claro,text_color=escuro)
    
    if not escolha:
        return
    
    medico, dados = buscar_medico_por_id(escolha)
    
    if not medico:
        sg.popup('Médico não encontrado!', title='Erro')
        return
    
    layout_edit = [
        [sg.Text('Editar Médico', font=('Helvetica', 14, 'bold'), background_color=claro, text_color=escuro)],
        [sg.Text(f'ID: {medico["id"]}', font=('Helvetica', 10), background_color=claro, text_color=escuro)],
        [sg.Text('Nome:'), sg.Input(default_text=medico['nome'], key='-NOME-', size=(30, 1), background_color=claro, text_color=escuro)],
        [sg.Text('Especialidade:'), sg.Input(default_text=medico['especialidade'], key='-ESPECIALIDADE-', size=(30, 1), background_color=claro, text_color=escuro)],
        [sg.Text('Disponível:'), sg.Text('Sim' if not medico.get('ocupado', False) else 'Não', key='-DISPONIVEL-', background_color=claro, text_color=escuro)],
        [sg.Button('Salvar Alterações', key='-SALVAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]
    
    window = sg.Window('Editar Médico', layout_edit, modal=True)
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return
        
        if event == '-SALVAR-':
            # Preserve the current availability (don't allow changing availability here)
            disponivel = not medico.get('ocupado', False)
            atualizar_medico(medico, values['-NOME-'], values['-ESPECIALIDADE-'], disponivel)
            salvar_dados('medicos.json', dados)
            sg.popup('Médico editado com sucesso!', title='Sucesso')
            window.close()
            return
        

def remover_medico():
    
    
    dados = carregar_dados('medicos.json')
    medicos = dados.get('medicos') if isinstance(dados, dict) else None
    if not medicos:
        sg.popup('Não há médicos registados!', title='Aviso')
        return
    
    escolha = sg.popup_get_text('Digite o ID do médico a remover:', title='Remover Médico')
    
    if not escolha:
        return
    
    medico, dados = buscar_medico_por_id(escolha)
    
    if not medico:
        sg.popup('Médico não encontrado!', title='Erro')
        return
    
    confirma = sg.popup_yes_no(f'Tem certeza que deseja remover {medico["nome"]}?', title='Confirmar Remoção')
    
    if confirma == 'Yes':
        if remover_medico_por_id(escolha):
            sg.popup('Médico removido com sucesso!', title='Sucesso')


def adicionar_paciente():
    
    layout_add = [
        [sg.Text('Adicionar Novo Paciente', font=('Helvetica', 14, 'bold'))],
        [sg.Text('ID:'), sg.Input(key='-ID-', size=(30, 1))],
        [sg.Text('Nome:'), sg.Input(key='-NOME-', size=(30, 1))],
        [sg.Text('Idade:'), sg.Input(key='-IDADE-', size=(30, 1))],
        [sg.Text('Sexo:'), sg.Combo(['masculino', 'feminino', 'outro'], key='-SEXO-', readonly=True)],
        [sg.Text('Doença:'), sg.Input(key='-DOENCA-', size=(30, 1))],
        [sg.Text('Prioridade:'), sg.Combo(['normal', 'alta', 'emergência'], key='-PRIORIDADE-', readonly=True)],
        [sg.Text('Atributos:', font=('Helvetica', 10, 'bold'))],
        [sg.Checkbox('Fumador', key='-FUMADOR-')],
        [sg.Checkbox('Consome Álcool', key='-ALCOOL-')],
        [sg.Text('Atividade Física:'), sg.Combo(['baixa', 'moderada', 'alta'], key='-ATIVIDADE-', readonly=True)],
        [sg.Checkbox('Doença Crónica', key='-CRONICO-')],
        [sg.Button('Guardar', key='-GUARDAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]
    
    window = sg.Window('Adicionar Paciente', layout_add, modal=True)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return
        
        if event == '-GUARDAR-':
            if not validar_campos_paciente(values['-ID-'], values['-NOME-'], values['-IDADE-'], 
                                          values['-SEXO-'], values['-DOENCA-'], 
                                          values['-PRIORIDADE-'], values['-ATIVIDADE-']):
                sg.popup('Por favor, preencha todos os campos!', title='Erro')
                continue
            
            idade, valido = validar_idade(values['-IDADE-'])
            if not valido:
                sg.popup('Idade deve ser um número!', title='Erro')
                continue
            
            novo_paciente = criar_paciente(
                values['-ID-'], values['-NOME-'], idade, values['-SEXO-'],
                values['-DOENCA-'], values['-PRIORIDADE-'], values['-FUMADOR-'],
                values['-ALCOOL-'], values['-ATIVIDADE-'], values['-CRONICO-']
            )
            adicionar_paciente_dados(novo_paciente)
            sg.popup('Paciente adicionado com sucesso!', title='Sucesso')
            window.close()
            return
        


def editar_paciente():
    
    dados = carregar_dados('pacientes.json')
    pacientes = dados.get('pacientes') if isinstance(dados, dict) else None
    if not pacientes:
        sg.popup('Não há pacientes registados!', title='Aviso')
        return
    
    escolha = sg.popup_get_text('Digite o ID do paciente:', title='Selecionar Paciente')
    
    if not escolha:
        return
    
    paciente, dados = buscar_paciente_por_id(escolha)
    
    if not paciente:
        sg.popup('Paciente não encontrado!', title='Erro')
        return
    
    layout_edit = [
        [sg.Text('Editar Paciente', font=('Helvetica', 14, 'bold'))],
        [sg.Text(f'ID: {paciente["id"]}', font=('Helvetica', 10))],
        [sg.Text('Nome:'), sg.Input(default_text=paciente['nome'], key='-NOME-', size=(30, 1))],
        [sg.Text('Idade:'), sg.Input(default_text=str(paciente['idade']), key='-IDADE-', size=(30, 1))],
        [sg.Text('Sexo:'), sg.Combo(['masculino', 'feminino', 'outro'], 
                                     default_value=paciente['sexo'], key='-SEXO-', readonly=True)],
        [sg.Text('Doença:'), sg.Input(default_text=paciente['doenca'], key='-DOENCA-', size=(30, 1))],
        [sg.Text('Prioridade:'), sg.Combo(['normal', 'alta', 'emergência'], 
                                          default_value=paciente['prioridade'], key='-PRIORIDADE-', readonly=True)],
        [sg.Text('Atributos:', font=('Helvetica', 10, 'bold'))],
        [sg.Checkbox('Fumador', default=paciente['atributos']['fumador'], key='-FUMADOR-')],
        [sg.Checkbox('Consome Álcool', default=paciente['atributos']['consome_alcool'], key='-ALCOOL-')],
        [sg.Text('Atividade Física:'), sg.Combo(['baixa', 'moderada', 'alta'], 
                                                 default_value=paciente['atributos']['atividade_fisica'], 
                                                 key='-ATIVIDADE-', readonly=True)],
        [sg.Checkbox('Doença Crónica', default=paciente['atributos']['cronico'], key='-CRONICO-')],
        [sg.Button('Salvar Alterações', key='-SALVAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]
    
    window = sg.Window('Editar Paciente', layout_edit, modal=True)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return
        
        if event == '-SALVAR-':
            idade, valido = validar_idade(values['-IDADE-'])
            if not valido:
                sg.popup('Idade deve ser um número!', title='Erro')
                continue
            
            atualizar_paciente(
                paciente, values['-NOME-'], idade, values['-SEXO-'],
                values['-DOENCA-'], values['-PRIORIDADE-'], values['-FUMADOR-'],
                values['-ALCOOL-'], values['-ATIVIDADE-'], values['-CRONICO-']
            )
            salvar_dados('pacientes.json', dados)
            sg.popup('Paciente editado com sucesso!', title='Sucesso')
            window.close()
            return
        

def remover_paciente():
    
    dados = carregar_dados('pacientes.json')
    pacientes = dados.get('pacientes') if isinstance(dados, dict) else None
    if not pacientes:
        sg.popup('Não há pacientes registados!', title='Aviso')
        return
    
    escolha = sg.popup_get_text('Digite o ID do paciente a remover:', title='Remover Paciente')
    
    if not escolha:
        return
    
    paciente, dados = buscar_paciente_por_id(escolha)
    
    if not paciente:
        sg.popup('Paciente não encontrado!', title='Erro')
        return
    
    confirma = sg.popup_yes_no(f'Tem certeza que deseja remover {paciente["nome"]}?', title='Confirmar Remoção')
    
    if confirma == 'Yes':
        if remover_paciente_por_id(escolha):
            sg.popup('Paciente removido com sucesso!', title='Sucesso')



def listar_medicos():
    tem_medicos, _ = verificar_dados_importados()
    
    if not tem_medicos:
        sg.popup('Não há médicos registados!', title='Aviso', 
                background_color=claro, text_color=escuro)
        return
    
    dados = carregar_dados('medicos.json')
    medicos = dados.get('medicos', [])

    # Cabeçalho da tabela
    cabecalho = f"{'ID':<8} {'Nome':<30} {'Especialidade':<25} {'Estado':<15}\n"
    cabecalho += "=" * 80 + "\n"
    
    # Construir linhas formatadas
    linhas = [cabecalho]
    for m in medicos:
        id_medico = m.get('id', '')
        nome = m.get('nome', '')
        especialidade = m.get('especialidade', '')
        ocupado = m.get('ocupado', False)
        
        # Status com emojis/símbolos
        if ocupado:
            status = '🔴 Ocupado'
            doente = m.get('doente_corrente', '')
            if doente:
                status += f' (atendendo {doente})'
        else:
            status = '🟢 Disponível'
        
        linha = f"{id_medico:<8} {nome:<30} {especialidade:<25} {status}\n"
        linhas.append(linha)
    
    # Adicionar estatísticas no final
    total_medicos = len(medicos)
    disponiveis = sum(1 for m in medicos if not m.get('ocupado', False))
    ocupados = total_medicos - disponiveis
    
    linhas.append("\n" + "=" * 80 + "\n")
    linhas.append(f"Total de Médicos: {total_medicos}  |  Disponíveis: {disponiveis}  |  Ocupados: {ocupados}\n")

    layout = [
        [sg.Text('Lista de Médicos', font=('Helvetica', 14, 'bold'), 
                background_color=claro, text_color=escuro, pad=(10,15))],
        [sg.Multiline(''.join(linhas), size=(85, 25), disabled=True, 
                     background_color='white', text_color=escuro, 
                     font=('Courier', 10), pad=(10,10))],
        [sg.Push(background_color=claro),
         sg.Button('Fechar', button_color=(claro, escuro), size=(12,1), 
                  font=('Helvetica', 10), pad=(10,10)),
         sg.Push(background_color=claro)]
    ]
    
    w = sg.Window('Médicos', layout, modal=True, background_color=claro, 
                 size=(750, 550), element_justification='center')
    e, v = w.read()
    w.close()


def listar_pacientes():
    _, tem_pacientes = verificar_dados_importados()
    
    if not tem_pacientes:
        sg.popup('Não há pacientes registados!', title='Aviso', 
                background_color=claro, text_color=escuro)
        return
    
    dados = carregar_dados('pacientes.json')
    pacientes = dados.get('pacientes', [])

    # Cabeçalho da tabela
    cabecalho = f"{'ID':<6} {'Nome':<30} {'Idade':<7} {'Sexo':<12} {'Prioridade':<13} {'Doença':<20}\n"
    cabecalho += "=" * 95 + "\n"
    
    # Construir linhas formatadas
    linhas = [cabecalho]
    
    # Ordenar por prioridade (emergência > alta > normal)
    ordem_prioridade = {'emergência': 0, 'alta': 1, 'normal': 2}
    pacientes_ordenados = sorted(pacientes, 
                                 key=lambda p: ordem_prioridade.get(p.get('prioridade', 'normal'), 3))
    
    for p in pacientes_ordenados:
        id_pac = p.get('id', '')
        nome = p.get('nome', '')
        idade = str(p.get('idade', ''))
        sexo = p.get('sexo', '').capitalize()
        prioridade = p.get('prioridade', '').upper()
        doenca = p.get('doenca', '')
        
        # Emoji/símbolo de prioridade
        if prioridade == 'EMERGÊNCIA':
            prioridade_str = '🔴 ' + prioridade
        elif prioridade == 'ALTA':
            prioridade_str = '🟠 ' + prioridade
        else:
            prioridade_str = '🟢 ' + prioridade
        
        linha = f"{id_pac:<6} {nome:<30} {idade:<7} {sexo:<12} {prioridade_str:<20} {doenca:<20}\n"
        linhas.append(linha)
    
    # Adicionar informações sobre atributos dos pacientes
    linhas.append("\n" + "=" * 95 + "\n")
    linhas.append("ATRIBUTOS DOS PACIENTES:\n")
    linhas.append("-" * 95 + "\n")
    
    for p in pacientes_ordenados:
        id_pac = p.get('id', '')
        nome = p.get('nome', '')
        atributos = p.get('atributos', {})
        
        atr_lista = []
        if atributos.get('fumador'): atr_lista.append('Fumador')
        if atributos.get('consome_alcool'): atr_lista.append('Consome Álcool')
        if atributos.get('cronico'): atr_lista.append('Doença Crónica')
        atr_lista.append(f"Ativ. Física: {atributos.get('atividade_fisica', 'N/A').capitalize()}")
        
        linha_atr = f"{id_pac} - {nome}: {', '.join(atr_lista)}\n"
        linhas.append(linha_atr)
    
    # Estatísticas
    linhas.append("\n" + "=" * 95 + "\n")
    total_pacientes = len(pacientes)
    emergencia = sum(1 for p in pacientes if p.get('prioridade') == 'emergência')
    alta = sum(1 for p in pacientes if p.get('prioridade') == 'alta')
    normal = sum(1 for p in pacientes if p.get('prioridade') == 'normal')
    
    linhas.append(f"Total: {total_pacientes}  |  🔴 Emergência: {emergencia}  |  🟠 Alta: {alta}  |  🟢 Normal: {normal}\n")

    layout = [
        [sg.Text('Lista de Pacientes', font=('Helvetica', 14, 'bold'), 
                background_color=claro, text_color=escuro, pad=(10,15))],
        [sg.Multiline(''.join(linhas), size=(100, 30), disabled=True, 
                     background_color='white', text_color=escuro, 
                     font=('Courier', 9), pad=(10,10))],
        [sg.Push(background_color=claro),
         sg.Button('Fechar', button_color=(claro, escuro), size=(12,1), 
                  font=('Helvetica', 10), pad=(10,10)),
         sg.Push(background_color=claro)]
    ]
    
    w = sg.Window('Pacientes', layout, modal=True, background_color=claro, 
                 size=(900, 650), element_justification='center')
    e, v = w.read()
    w.close()







def abrir_menu():
    window = sg.Window('Menu Principal', layout, background_color=claro, size=(500, 500), element_justification='center')

    while True:
        event, values = window.read()

        # Fechar janela
        if event == sg.WIN_CLOSED or event is None:
            window.close()
            return

        # Evento: Simulação Clínica
        if event == '-SIMULACAO-':
            sg.popup('Funcionalidade de Simulação Clínica será implementada em breve!', title='Simulação Clínica')

        # Evento: Alterar Dados
        elif event == '-ALTERAR-':
            dados_medicos = carregar_dados('medicos.json')
            dados_pacientes = carregar_dados('pacientes.json')
            tem_medicos = bool(dados_medicos.get('medicos')) if isinstance(dados_medicos, dict) else False
            tem_pacientes = bool(dados_pacientes.get('pacientes')) if isinstance(dados_pacientes, dict) else False
            if not tem_medicos and not tem_pacientes:
                popup_ok('Não há dados na base. Importe médicos ou pacientes antes de alterar.', title='Aviso', background_color=claro, button_color=(claro, escuro), text_color=escuro)
                continue
            window.hide()
            alterar_dados()
            window.un_hide()

        elif event == '-IMPORTAR-':
            importar_dados()

        # Evento: Sair
        elif event == '-SAIR-':
            resposta = popup_sim_nao('Tem certeza que deseja sair?',text_color=escuro, title='Confirmar Saída')
            if resposta == 'Sim':
                popup_ok('Obrigado por utilizar o Sistema de Gestão Clínica!\nAté breve!', title='Agradecimento', background_color=claro, button_color=(claro, escuro), text_color=escuro)
                window.close()
                return


if __name__ == '__main__':
    abrir_menu()