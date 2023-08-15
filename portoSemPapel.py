import sqlite3
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from time import sleep
import getpass
import logging
import logging

login= "XXXXXXXXXXXXXX"
senha= "XXXXXXXXXXXXX"
navegador = webdriver.Chrome()
def login():
    aux=0
    while True:
        navegador.delete_all_cookies()
        navegador.get('https://concentrador.portosempapel.gov.br/portal/login.html')
        sleep(10)
        navegador.find_element(By.ID, 'cpf').send_keys(login)
        
        navegador.find_element(By.ID, 'senha').send_keys(senha)
        
        navegador.find_element(By.ID, 'btnLogar').click()
     
        sleep(20)

def scraping_dados():

    login 
    banco = sqlite3.connect('PortoSemPapel.db')
    cursor = banco.cursor()
    today = date.today().strftime("%d%m%y")
    table_name = f"portoSemPapel_{today}"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (navio text, bandeira text,  comCal text, nav text, chegada text, carimbo text, agencia text, operacao text, tipo text, peso text, viagem text, p text, terminal text)") 
    
    options = Options()
    navegador = webdriver.Chrome(options=options)

    try:
        navegador.get('https://concentrador.portosempapel.gov.br/portal/login.html')
    except WebDriverException:
        print('Erro ao acessar o site. Tentando novamente em 20 minutos...')
        navegador.quit()
        time.sleep(1200) 
        return scraping_dados()
        
    soup = BeautifulSoup(navegador.page_source, 'html.parser')
    
    def atualizardados(navio,bandeira, comCal, nav, chegada, carimbo, agencia, operacao, tipo, peso, viagem, p, terminal ):
        cursor.execute(f"INSERT INTO {table_name} (navio,bandeira, comCal, nav, chegada, carimbo, agencia, operacao, tipo, peso, viagem, p, terminal ) VALUES ('{navio}','{bandeira}','{comCal}','{nav}', '{chegada}','{carimbo}','{agencia}', '{operacao}','{tipo}', '{peso}', '{viagem}','{p}','{terminal}')")
        banco.commit()

    for linha in soup.findAll( 'tr', class_='text-center'):
        navio = linha.findAll('td')[0].text
        bandeira = linha.findAll('td')[1].text
        comCal = linha.findAll('td')[2].text
        nav = linha.findAll('td')[3].text
        chegada= linha.findAll('td')[4].text
        carimbo= linha.findAll('td')[5].text
        agencia = linha.findAll('td')[6].text
        operacao = linha.findAll('td')[7].text
        tipo = linha.findAll('td')[8].text
        peso = linha.findAll('td')[9].text
        viagem = linha.findAll('td')[10].text
        p = linha.findAll('td')[11].text
        terminal = linha.findAll('td')[12].text

        atualizardados(navio,bandeira, comCal, nav, chegada, carimbo, agencia, operacao, tipo, peso, viagem, p, terminal )

    dados = pd.read_sql_query(f"SELECT * from {table_name}", banco)
    dados.to_excel(f"PortoSemPapel_{today}.xlsx", index=False)
    navegador.quit()
    banco.close()
    time.sleep(600)

while True:
    scraping_dados()
    entrada = input("Digite 'parar' para encerrar o script: ")
    if entrada == "parar":
        break
