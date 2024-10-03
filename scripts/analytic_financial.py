import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

while True:

    #Pergunta ao usuário qual site gostaria de realizar as análises dos relatórios
    site_escolhido = input('Aperte 1 para escolher o "Banco Itaú", ' 
                           'Aperte 2 para escolher o "Banco Inter", '
                           'e Aperte 3 para escolher o "Banco do Brasil": ')

    if site_escolhido in ['1', '2', '3']:

        # Configuração do WebDriver (Chrome neste caso)
        #Criando um serviço responsável por instalar a versão do chrome driver de forma automática
        service = Service(ChromeDriverManager().install())

        #Executando este serviço
        driver = webdriver.Chrome(service=service)
        print('Chrome driver configurado com sucesso.')


        if site_escolhido == '1':
            # Acessando o site de RI do Itaú
            driver.get('https://www.itau.com.br/relacoes-com-investidores/resultados-e-relatorios/central-de-resultados/')
            print('RPA entrou corretamente na central de resultados do itaú')
        elif site_escolhido == '2':
            # Acessando o site de RI do Inter
            driver.get('https://investors.inter.co/informacoes-aos-investidores/central-de-resultados-inter-co/')
            print('RPA entrou corretamente na central de resultados do inter')
        elif site_escolhido == '3':
             # Acessando o site de RI do Banco do Brasil
            driver.get('https://ri.bb.com.br/informacoes-financeiras/central-de-resultados/')
            print('RPA entrou corretamente na central de resultados do Banco do Brasil')
            
        #Sai do loop    
        break
    else:
        print('Escolha um número entre 1 e 3')
