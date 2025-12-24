import FreeSimpleGUI as sg
from funcoes import *

escuro='#2196f3'
claro='#c3e3fd'



# Layout do menu principal
layout = [
    [sg.Text('Sistema de Gestão Clínica', background_color=claro, text_color=escuro,
             font=('Helvetica', 20, 'bold'), justification='center', expand_x=True)],

    # Espaçamento para centralizar verticalmente
    [sg.Text(background_color=claro, size=(1,2))],

    # Botões grandes centrados horizontalmente
    [sg.Text('', background_color=claro, size=(8,1)), sg.Button('Simulação Clínica', button_color=(claro, escuro), size=(32, 4), font=('Helvetica', 12), key='-SIMULACAO-'), sg.Text('', background_color=claro, size=(10,2))],
    [sg.Text('', background_color=claro, size=(8,1)), sg.Button('Alterar Dados', button_color=(claro, escuro), size=(32, 4), font=('Helvetica', 12), key='-ALTERAR-'), sg.Text('', background_color=claro, size=(10,2))],
    [sg.Text('', background_color=claro, size=(8,1)), sg.Button('Importar Dados', button_color=(claro, escuro), size=(32, 4), font=('Helvetica', 12), key='-IMPORTAR-'), sg.Text('', background_color=claro, size=(10,2))],
    # Espaçamento antes do botão de sair
    [sg.Text(background_color=claro, size=(0,0))],

    # Botão de Saída (menor) centrado
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



def adicionar_medico():
    
    layout_add = [
        [sg.Text('Adicionar Novo Médico', font=('Helvetica', 14, 'bold'))],
        [sg.Text('ID:'), sg.Input(key='-ID-', size=(30, 1))],
        [sg.Text('Nome:'), sg.Input(key='-NOME-', size=(30, 1))],
        [sg.Text('Especialidade:'), sg.Input(key='-ESPECIALIDADE-', size=(30, 1))],
        [sg.Text('Disponível:'), sg.Combo(['Sim', 'Não'], default_value='Sim', key='-DISPONIVEL-', readonly=True)],
        [sg.Button('Guardar', key='-GUARDAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]
    
    window = sg.Window('Adicionar Médico', layout_add, modal=True)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return
        
        if event == '-GUARDAR-':
            if not validar_campos_medico(values['-ID-'], values['-NOME-'], values['-ESPECIALIDADE-']):
                sg.popup('Por favor, preencha todos os campos!', title='Erro')
                continue
            
            disponivel = values['-DISPONIVEL-'] == 'Sim'
            novo_medico = criar_medico(values['-ID-'], values['-NOME-'], values['-ESPECIALIDADE-'], disponivel)
            adicionar_medico_dados(novo_medico)
            sg.popup('Médico adicionado com sucesso!', title='Sucesso')
            window.close()
            return


def editar_medico():
    """Interface para editar médico existente"""
    dados = carregar_dados('medicos.json')
    if not dados['medicos']:
        sg.popup('Não há médicos registados!', title='Aviso')
        return
    
    escolha = sg.popup_get_text('Digite o ID do médico:', title='Selecionar Médico')
    
    if not escolha:
        return
    
    medico, dados = buscar_medico_por_id(escolha)
    
    if not medico:
        sg.popup('Médico não encontrado!', title='Erro')
        return
    
    layout_edit = [
        [sg.Text('Editar Médico', font=('Helvetica', 14, 'bold'))],
        [sg.Text(f'ID: {medico["id"]}', font=('Helvetica', 10))],
        [sg.Text('Nome:'), sg.Input(default_text=medico['nome'], key='-NOME-', size=(30, 1))],
        [sg.Text('Especialidade:'), sg.Input(default_text=medico['especialidade'], key='-ESPECIALIDADE-', size=(30, 1))],
        [sg.Text('Disponível:'), sg.Combo(['Sim', 'Não'], 
                                          default_value='Não' if medico['ocupado'] else 'Sim', 
                                          key='-DISPONIVEL-', readonly=True)],
        [sg.Button('Salvar Alterações', key='-SALVAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
    ]
    
    window = sg.Window('Editar Médico', layout_edit, modal=True)
    
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return
        
        if event == '-SALVAR-':
            disponivel = values['-DISPONIVEL-'] == 'Sim'
            atualizar_medico(medico, values['-NOME-'], values['-ESPECIALIDADE-'], disponivel)
            salvar_dados('medicos.json', dados)
            sg.popup('Médico editado com sucesso!', title='Sucesso')
            window.close()
            return
        

def remover_medico():
    """Interface para remover médico"""
    dados = carregar_dados('medicos.json')
    if not dados['medicos']:
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
    """Interface para adicionar novo paciente"""
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
    """Interface para editar paciente existente"""
    dados = carregar_dados('pacientes.json')
    if not dados['pacientes']:
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
    """Interface para remover paciente"""
    dados = carregar_dados('pacientes.json')
    if not dados['pacientes']:
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






def alterar_dados():
    
    
    dados_medicos = carregar_dados('medicosnovo.json')
    dados_pacientes = carregar_dados('pacientes.json')
    tem_medicos = bool(dados_medicos.get('medicos'))
    tem_pacientes = bool(dados_pacientes.get('pacientes'))
    if not tem_medicos and not tem_pacientes:
        popup_ok('Não há dados na base. Importe médicos ou pacientes antes de alterar.', title='Aviso', background_color=claro, button_color=(escuro, claro), text_color=escuro)
        return
    

    coluna_medicos = [
        [sg.Text('Gestão de Médicos', font=('Helvetica', 12, 'bold'), justification='center')],
        [sg.Text('')],
        [sg.Button('Adicionar Médico', size=(20, 2), key='-ADD-MEDICO-')],
        [sg.Text('')],
        [sg.Button('Editar Médico', size=(20, 2), key='-EDIT-MEDICO-')],
        [sg.Text('')],
        [sg.Button('Remover Médico', size=(20, 2), key='-REM-MEDICO-', button_color=('white', 'dark red'))]
    ]
    
    
    coluna_pacientes = [
        [sg.Text('Gestão de Pacientes', font=('Helvetica', 12, 'bold'), justification='center')],
        [sg.Text('')],
        [sg.Button('Adicionar Paciente', size=(20, 2), key='-ADD-PACIENTE-')],
        [sg.Text('')],
        [sg.Button('Editar Paciente', size=(20, 2), key='-EDIT-PACIENTE-')],
        [sg.Text('')],
        [sg.Button('Remover Paciente', size=(20, 2), key='-REM-PACIENTE-', button_color=('white', 'dark red'))]
    ]
    
    
    layout = [
        [sg.Text('Alteração de Dados', font=('Helvetica', 16, 'bold'), justification='center', expand_x=True)],
        [sg.HorizontalSeparator()],
        [sg.Text('')],
        [sg.Column(coluna_medicos, element_justification='center', vertical_alignment='top'), 
         sg.VerticalSeparator(),
         sg.Column(coluna_pacientes, element_justification='center', vertical_alignment='top')],
        [sg.Text('')],
        [sg.HorizontalSeparator()],
        [sg.Button('Voltar ao Menu', size=(15, 1), key='-VOLTAR-')]
    ]
    
    window = sg.Window('Alteração de Dados', layout, size=(650, 450), element_justification='center')
    
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




def importar_dados():
    
    caminho_medicos = sg.popup_get_file(
    'Escolha o ficheiro de médicos',
    file_types=(('JSON Files', '*.json'),),
    initial_folder='.',
    save_as=False
    )

    if not caminho_medicos:
        return

    
    caminho_pacientes = sg.popup_get_file(
    'Escolha o ficheiro de pacientes',
    file_types=(('JSON Files', '*.json'),),
    initial_folder='.',
    save_as=False
    )

    if not caminho_pacientes:
        return

    dados_medicos = carregar_dados(caminho_medicos)
    dados_pacientes = carregar_dados(caminho_pacientes)

    # validações simples
    if 'medicos' not in dados_medicos:
        sg.popup('Ficheiro de médicos inválido!', title='Erro')
        return

    if 'pacientes' not in dados_pacientes:
        sg.popup('Ficheiro de pacientes inválido!', title='Erro')
        return

    # guardar como base oficial da aplicação
    salvar_dados('medicos.json', dados_medicos)
    salvar_dados('pacientes.json', dados_pacientes)

    sg.popup('Dados importados com sucesso!', title='Sucesso')





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