#!/usr/bin/env python3
# coding: utf-8

# In[5]:


import time


# In[20]:


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


# In[3]:


input('pressione enter para continuar se o Whatsapp Web já estiver aberto: \n')

input('o cardapio ja esta na area de copia? (ctrl+c & ctrl+v): \n')


# In[1]:


def scrollChats_to_end():
    try:
        chatList = driver.find_elements_by_class_name('_1H6CJ')
        driver.execute_script("arguments[0].scrollIntoView(false);", chatList[0])
    except:
        print('algo deu errado ao dar scroll')


# In[ ]:


def clic_contact():
    try:
        driver.find_elements_by_css_selector('span._3NWy8')[-1].click()
        return True
    except Exception as error:
        print(type(error))
        print(error)
        return False


# In[5]:


def total_conversations():
    try:
        chat_list = driver.find_elements_by_class_name('X7YrQ')
        
        total = 0
        for chat in chat_list:
            starter = chat.get_attribute('style').find(':')
            delimiter = chat.get_attribute('style').find(';')
            found = int(''.join(filter(str.isdigit, chat.get_attribute('style')[starter:delimiter])))
            if found > total:
                total = found
        return total
    except:
        return 'Total Not Found'


# In[9]:


def sendImage(name):
    try:
        driver.find_element_by_class_name('_3u328').send_keys(Keys.CONTROL + "v")
        time.sleep(1)
        driver.find_element_by_class_name('_3u328').send_keys(Keys.ENTER)
        enviados.append(name)
        return True
    except Exception as error:
        print(type(error))
        print(error)
        return False


# In[19]:


#pegar numero de conversas e contar quantas ja foram enviadas
chats = total_conversations()
count = 0
enviados = []
while count < (chats - 2): #-2 porque tem dois grupos para os quais nao conseguira enviar
    time.sleep(1)
    scrollChats_to_end()
    time.sleep(1.5)
    name = driver.find_element_by_xpath("//div[@class='_19vo_']").text
    if clic_contact() and name not in enviados:
        time.sleep(0.5)
        print('enviado cardapio para: {}'.format(count, name))
        sendImage(name)
        count +=1

