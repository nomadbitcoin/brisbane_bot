#!/usr/bin/env python
# coding: utf-8

# In[4]:


import bs4
import time
import os
import random


# In[3]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys

#instance headless
options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('--window-size-1920x1080')

# open with saved informations in cache
options.add_argument("profile")
options.add_argument("user-data-dir=./whatsapp_nabike")

driver = webdriver.Chrome(options=options, executable_path="./webdriver/chromedriver")
driver.get('https://web.whatsapp.com/')


# In[ ]:


input('pressione enter se o Whatsapp Web já estiver aberto: \n')


# In[3]:


def scrollChats_to_end():
    try:
        chatList = driver.find_elements_by_class_name('_1H6CJ')
        driver.execute_script("arguments[0].scrollIntoView(false);", chatList[0])
    except:
        print('algo deu errado ao dar scroll')


# In[4]:


def controlConection(up_or_down):
    try:
        sudoPassword = 'kaisen'
        command = 'sudo ip link set enp7s0 '+ str(up_or_down)
        os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        time.sleep(5)
    except:
        print('Erro conexao')


# In[5]:


def sendImage():
    rounds = 0
    for contact in driver.find_elements_by_xpath("//div[@class='X7YrQ']"):
        try:
            name = contact.find_elements_by_css_selector('span._3NWy8')[0].text
            #verifica quando foi a ultima mensagem enviada para o contato, se houver " : " eh porque recebeu mensagem no mesmo dia entao nao recebera o cardapio novamente
            #when = contact.find_elements_by_css_selector('div._0LqQ')[0].text.find(':')
            #se o identificador de horario nao for encontrado o find retorna -1
    
            print('enviando cardapio para: {}'.format(name))
            try:
                contact.find_elements_by_css_selector('span._3NWy8')[0].click()
                time.sleep(1)
                driver.find_element_by_xpath("//div[@class='_13mgZ']").send_keys(Keys.CONTROL + "v")
                time.sleep(1)
                driver.find_element_by_xpath("//div[@class='rK2ei USE1O']").find_element_by_xpath("//div[@class='iA40b']").click()
                enviados.append(name)
            except KeyboardInterrupt:
                print('stopped Sender')
                break
            except:
                print('houve algum problema')
                nao_enviados.append(name)
                pass
            time.sleep(1)
            rounds +=1
        except:
            pass
    return rounds


# In[ ]:


enviados = []
nao_enviados = []
while True:
    try:
        shipped = 0
        scrollChats_to_end()
        controlConection('down')
        
        #define um numero aleatorio de cardapios para enviar a cada conexao
        num_sends = int(random.randint(69,99))
        
        while shipped <= num_sends:
            shipped = shipped + sendImage()

        # escolhe um tempo aleatorio em segundos entre 50 e 80s para que os cardapios sejam enviados apos conexao com internet
        controlConection('up')
        
        time_to_wait = int(random.randint(50,80))
        print('sending files...')
        
        time.sleep(time_to_wait)
        print('\n{} enviados ate o momendo'.format(len(enviados)))
            
    except KeyboardInterrupt:
        print('stopped everything')
        break


# In[6]:


# controlConection('up')


# In[ ]:


#TO DO
#verica se ha o reloginho de enviando, se sim, clica no proximo contato, senao, insere em nao enviados
#apos conexao verifica se as conversas tem o sinal de enviado, se sim, desliga e scrolla enviar

