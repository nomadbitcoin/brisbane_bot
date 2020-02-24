#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time
import bs4
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# In[3]:


wait = 1


# In[4]:


# INSTANCE BROWSER
def openBrowser(business):
    '''
        Verifica qual o sistema operacional para que use o driver e diretorio de usuarios certo
    '''
    
    if platform.system() == 'Linux':
        driver_path = './webdriver/linux/chromedriver'
        profile_path = '/home/nomadbitcoin/whatsapp_profiles/' + business 
    elif platform.system() == 'Windows':
        driver_path = r'C:\\Users\\Yan\\Desktop\\brisbane_bot\\webdriver\\win\\chromedriver.exe'
        profile_path = "C:\\Users\\Yan\\Desktop\\brisbane_bot\\profiles\\" + business
        print(profile_path)
    
    
    global driver
    try:
        options = webdriver.ChromeOptions()
        # open with saved informations in cache
        options.add_argument("profile")
        options.add_argument("user-data-dir=" + profile_path)
        driver = webdriver.Chrome(options=options, executable_path=driver_path)
#         driver.implicitly_wait(5) #tempo implicito de espera 1 segundo antes de cada acao
        main_url = 'https://web.whatsapp.com/'
        driver.get(main_url)
        if wait_connection(driver):
            return True, 'opened in: {}'.format(main_url)
    except Exception as error:
        print(type(error), error)
        return False
    
# PARA LIBERAR SOMENTE APOS TER ABERTO O WHATSAPP
def wait_connection(driver):
    waiting = True
    while waiting:
        try:
            if driver.find_element_by_class_name('Qk8nZ').text == 'Keep your phone connected':
                waiting = False
                return True
                break
#             elif driver.find_element_by_class_name('_13HPh').text == 'Computer not connected':
#                 waiting = False
#                 return False, 'Computer not connected'
        except KeyboardInterrupt:
            waiting = False
            return False
        except:
            time.sleep(10)
            pass


# In[5]:


def scrollChats_to_end():
    try:
        chatList = driver.find_elements_by_class_name('_1H6CJ')
        driver.execute_script("arguments[0].scrollIntoView(false);", chatList[0])
    except Exception as error:
        print(type(error), error)
        print('algo deu errado ao dar scroll')


# In[6]:


def click_contact():
    try:
        driver.find_elements_by_css_selector('span._3NWy8')[-1].click()
        name = get_name()
        return name
    except Exception as error:
        print(type(error), error)
        return False
    
def get_name():
    try:
        name = driver.find_element_by_xpath("//div[@class='_19vo_']").text
        return name
    except Exception as error:
        print(type(error), error)        
        return 'None'


# In[7]:


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
    except Exception as error:
        print(type(error), error)
        return 'Total Not Found'


# In[8]:


def sendImage(name):
    try:
        driver.find_element_by_class_name('_3u328').send_keys(Keys.CONTROL + "v")
        time.sleep(wait)
        driver.find_element_by_class_name('_3u328').send_keys(Keys.ENTER)
        enviados.append(name)
        return True
    except Exception as error:
        print(type(error), error)
        return False


# In[ ]:


openBrowser('33sushihouse')


# In[ ]:


input('Continue se Whatsapp esta aberto e conteudo estiver na area ctrl+c & ctrl+v: \n')


# In[ ]:


#pegar numero de conversas e contar quantas ja foram enviadas
chats = total_conversations()
count = 0
enviados = []
while count <= chats: #-2 porque tem dois grupos para os quais nao conseguira enviar
    try:
        time.sleep(wait)
        scrollChats_to_end()
        time.sleep(wait)
        name = click_contact()
        assert name != False, 'Nao conseguiu clicar no contato'
        if name not in enviados:
            time.sleep(wait)
            print('{} de {} // Enviando para: {}'.format(count, chats,name))
            sendImage(name)
            count +=1
    except Exception as error:
        print(type(error), error)
        
print('\n\n ---------- TODOS ENVIADOS ---------- total [{}]\n\n'.format(count))


# ## Envio atraves de encaminhamento

# In[103]:


# PEGA A UNICA MENSAGEM QUE HA NO CHAT 'TO_SEND' - FUNCIONANDO PARA IMAGENS
def click_forward(content, have_text=False):
    '''
        Deve Haver uma conversa com as mensagens a serem encaminhadas e NADA MAIS,
        pode ser um grupo sozinho ou uma conversa com alguem mas 
        é essencial que não tenha mais nenhuma mensagem na conversa além das mensagens a serem encaminnhadas
    
        o conteudo pode ser imagem, audio, video, ou texto e caso seja imagem ou video pode conter texto
    '''
    
    # se o conteudo a ser encaminhado for imagem
    if content == 'image':
        try:
            div_chat = driver.find_element_by_class_name('_1ays2')
            mensagens = div_chat.find_elements_by_class_name('FTBzM')
            for msg in mensagens:
                try:
                    #verifica se ha imagem a ser verificada e verifica se ja foi verificada
                    src = msg.find_element_by_tag_name('img').get_attribute('src')
                    msg.find_element_by_xpath('//span[@data-icon="forward-chat"]').click()
                    #retorna True para o clique e tambem o conteudo de texto da mensagem, senao somente True
                    text = msg.text[:-8]if have_text == True else None
                    return True, text #os ultimos 8 caracteres sao o horario da mensagem e nao devem ser enviados
                except Exception as error:
                    if 'Unable to locate element' not in str(error):
                        print(type(error), error)
                    pass

        except Exception as error:
            print(type(error), error)


# In[140]:


def click_to_send():
    try:
        driver.find_element_by_xpath('//div[@data-animate-btn="true"]').click()
        return True
    except Exception as error:
        print(type(error), error)
        return False


# In[105]:


click_forward('image')


# In[140]:


def getChats():
    '''
        Pega a lista de chats apos clicar no botao de encaminhar
    '''
    chats = driver.find_elements_by_class_name('_2UaNq')
    return chats


# In[141]:


def isGroup(chat):
    '''
        Rececebe um chat e verifica se eh um grupo
    
        Quado eh grupo nao tera uma div especifica, entao retornara False
    '''
    try:
        div_contact = chat.find_element_by_class_name('_3NWy8')
        return False
    except Exception as error:
        if 'Unable to locate element' not in str(error):
            print(type(error), error)
        else:
            return True


# In[297]:


def clickChat(chat):
    try:
        chat.click()
        return True
    except Exception as error:
        return False

def select_contacts(groups=False):
    '''
        Verifica se os chats sao grupo, ira selecionar 5 chats que nao sejam grupos
    '''
    try:
        # caso nao seja para encaminhar para os grupos
        if groups == False:
            selected = 0
            for chat in getChats():
                time.sleep(wait)
                if not isGroup(chat) and clickChat(chat) and selected <=5:
                    print('{} selected: {}'.format(selected, chat.text))
                    selected +=1
                elif selected >=5:
                    break
            return True
        # se for para selecionar grupos eh a mesma coisa mais nao ira verificar antes se eh grupo
        else:
            selected = 0
            for chat in getChats():
                time.sleep(wait)
                if clickChat(chat) and selected <=5:
                    print('{} selected: {}'.format(selected, chat.text))
                    selected +=1
                elif selected >=5:
                    break
            return True
            
    except Exception as error:
        print(type(error), error)


# In[184]:


def scrollChats():
    '''
        Ira controlar os scrolls a serem dados na lista de chats
    '''
    pass


# In[273]:


# FUNCOES DE NAVEGACAO PELO WHATSAPP COM CLIQUES E TECLAS DO TECLADO
def down_chat(force=False, page_down=True):
    #force = True ira clicar na caixa de pesquisa e reiniciar o processo de clicar nos botoes
    if 'press_down' not in globals() or force == True:
        # CLICA NA CAIXA DE PESQUISA DE CONVERSAS
        driver.find_element_by_class_name('_2zCfw').click()
        
        # PRESSIONA A TECLA DOWN PARA NAVEGAR ENTRE AS CONVERSAS
        global press_down
        press_down = ActionChains(driver)
        press_down.send_keys(Keys.DOWN)
        press_down.perform()
    elif page_down == True:
        press_down.send_keys(Keys.PAGE_DOWN)
        press_down.perform()
    else:
        press_down.perform()


# In[291]:


down_chat()
time.sleep(wait)
select_contacts()


# In[294]:


total_conversations()


# In[298]:


# CLICA EM ENCAMINHAR MENSAGEM
def click_forward():
    '''
        Verifica se a ultima mensagem foi a propria conta que enviou e se eh uma imagem e se o tempo esta valido,
        apos clicar em encaminhar ira aguardar ate que o reloginho de enviando conclua
        tempo valido sera se o horario atual comparado ao tempo que esperou enviar coincide com o horario da imagem enviada
        (para casos em que a conta ja tenha enviado uma imagem antes)
    '''
    pass


# In[ ]:


#implementar relatorio de enviados em csv

