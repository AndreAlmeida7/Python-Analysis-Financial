# Importação de bibliotecas relevantes para o projeto
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox

#Pergunta ao usuário qual ativo gostaria de identificar seus indicadores
ativos = input('Escreva o nome da empresa ou o ticker da bolsa de valores que deseja identificar seus indicadores: ')

#Retira os espaços em branco dos ativos e deixa-os todos com letra maiúscula
ativos_formatados = [ativo.strip().upper() for ativo in ativos.split(",")] 
print(f'Seus ativos são: {ativos_formatados}')

# Função para exibir o pop-up de aviso
def mostrar_aviso():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    messagebox.showwarning("Aviso", "Este código é um robô que abrirá páginas web automaticamente, favor não fechá-las.")
    root.destroy()

# Chama a função para mostrar o pop-up no início do código
mostrar_aviso()

# Configuração do WebDriver (Chrome neste caso)
#Criando um serviço responsável por instalar a versão do chrome driver de forma automática
service = Service(ChromeDriverManager().install())
#Executando este serviço
navegador = webdriver.Chrome(service=service)

#Entrando no site statusinvest
navegador.get('https://statusinvest.com.br/')
# sleep(15) #espera 15 segundos para que a propagando apareça

# #Clicando para fechar a propaganda
# navegador.find_element(By.XPATH, '/html/body/div[19]/div/div/div[1]/button/i').click()

# Criando o cabeçalho do PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Times", 'B', 20)
pdf.cell(200,10,'Indicadores financeiros', ln=True, align='C')
pdf.set_line_width(0.5)  # Espessura da linha
pdf.line(70, 18, 150, 18)  # Desenho da linha (especifica a posição)
pdf.ln(5)  # Adiciona um espaço abaixo do cabeçalho

def adicionar_linha_separadora():
    pdf.set_line_width(1.0)  # Define a espessura da linha
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Desenha uma linha horizontal no PDF
    pdf.ln(5)  # Adiciona um espaço abaixo da linha

def adicionar_rodape():
    pdf.set_y(-10)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, 'Projeto realizado por André Almeida - Git: AndreAlmeida7', 0, 0, 'C')


#Para cada ativo dentro da lista de ativos que o usuário digitou faça o seguinte:
for ativo in ativos_formatados:
    
    #clicando na bússula de pesquisa
    navegador.find_element(By.XPATH, '//*[@id="main-nav-nav"]/div/div[2]/div/ul/li[2]/a/i').click()

    #Colocando o ativo dentro da barra de pesquisa
    navegador.find_element(By.XPATH, '//*[@id="main-search"]/div[1]/span[1]/input[2]').send_keys(ativo)

    sleep(5) #aguardando 5 segundos para carregar o nome do ativo

    #Se o usuário digitou o ativo de forma incorreta o código finaliza
    try:
        if navegador.find_element(By.XPATH, '//*[@id="main-search"]/div[2]/div/div/h4').text == "Não conseguimos encontrar nada com esta descrição...":
            pdf.set_font("Arial", '', 16)
            pdf.multi_cell(0, 10, f'Não foi possível encontrar o ativo {ativo}, favor validar.')
            break

    except:
        #Clicando no ativo desejado
        navegador.find_element(By.XPATH, '//*[@id="main-search"]/div[2]/div/div/a').click()

        # Faz a distinção de tipo de ativo, entre Fundo imobiliário e Ação
        if navegador.find_element(By.XPATH, '//*[@id="main-header"]/div[2]/div/div[1]/div/ol/li[2]/a/span').text == "Fundos Imobiliários":
         
            #Identificando os principais indicadores da página
            fundo_imobiliario = navegador.find_element(By.XPATH, '//*[@id="main-header"]/div[2]/div/div[1]/div/ol/li[2]/a/span').text
            dividend_yield = navegador.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div[1]/div[4]/div/div[1]/strong').text
            p_pv = navegador.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div[5]/div/div[2]/div/div[1]/strong').text
            numero_cotistas = navegador.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div[5]/div/div[6]/div/div[1]/strong').text
            valor_mercado = navegador.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div[5]/div/div[2]/div/div[2]/span[2]').text
            valor_caixa = navegador.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div[5]/div/div[3]/div/div[2]/span[2]').text
            valor_patrimonio_total = navegador.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div[5]/div/div[1]/div/div[2]/span[2]').text

            pdf.set_font("Arial", 'B', 12)
            pdf.multi_cell(0, 10, f'Ativo: {ativo} (Fundo Imobiliário)')
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 10, f'Dividend Yield: {dividend_yield}%\nP/PV: {p_pv}\nCotistas: {numero_cotistas}\n'
                                  f'Valor de Mercado: {valor_mercado}\nCaixa: {valor_caixa}\nPatrimônio Total: {valor_patrimonio_total}\n')
         
            
        else:
            acao = navegador.find_element(By.XPATH, '//*[@id="main-header"]/div[2]/div/div[1]/div/ol/li[2]/a/span').text
            dividend_yield = navegador.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div/div[1]/div/div[4]/div/div[1]/strong').text 
            valorizacao = navegador.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div/div[1]/div/div[5]/div/div[1]/strong').text 
            liquidez_diaria = navegador.find_element(By.XPATH, '//*[@id="main-2"]/div[2]/div/div[5]/div/div/div[3]/div/div/div').text 
            P_l = navegador.find_element(By.XPATH, '//*[@id="indicators-section"]/div[2]/div/div[1]/div/div[2]/div/div/strong').text 
            ev_ebitda = navegador.find_element(By.XPATH, '//*[@id="indicators-section"]/div[2]/div/div[1]/div/div[5]/div/div/strong').text
            divida_ebitda = navegador.find_element(By.XPATH, '//*[@id="indicators-section"]/div[2]/div/div[2]/div/div[2]/div/div/strong').text
            margem_liquida = navegador.find_element(By.XPATH, '//*[@id="indicators-section"]/div[2]/div/div[3]/div/div[4]/div/div/strong').text
            roe = navegador.find_element(By.XPATH, '//*[@id="indicators-section"]/div[2]/div/div[4]/div/div[1]/div/div/strong').text

            pdf.set_font("Arial", 'B', 12)
            pdf.multi_cell(0, 10, f'Ativo: {ativo} (Ação)')
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 10, f'Dividend Yield: {dividend_yield}%\nValorização: {valorizacao}\nLiquidez Diária: {liquidez_diaria}\n'
                                  f'P/L: {P_l}\nEV/EBITDA: {ev_ebitda}\nDívida/EBITDA: {divida_ebitda}\nMargem Líquida: {margem_liquida}\nROE: {roe}\n')
            
        adicionar_linha_separadora()

adicionar_rodape()

# Salvar o PDF
pdf_output = r'C:\Users\André Almeida\Desktop\indicadores_financeiros.pdf'
pdf.output(pdf_output)
print(f'O relatório foi salvo como {pdf_output}')