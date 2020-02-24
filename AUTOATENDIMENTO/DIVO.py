#!/usr/bin/env python3
# coding: utf-8

# In[22]:


import time
import platform
from datetime import datetime


# In[4]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys


# In[20]:


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
            engine_text = ['Mantenha seu celular conectado', 'Keep your phone connected']
            if driver.find_element_by_class_name('Qk8nZ').text in engine_text:
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


# In[6]:


def findUnreadChats():
    # PEGA AS CONVERSAS E SALVA SOMENTE AS QUE NAO FORAM LIDAS AINDA
    chats = driver.find_elements_by_class_name('_2UaNq')

    unread_chats = []
    for chat in chats:
        try:
            chat.find_element_by_class_name('P6z4j')
            unread_chats.append(chat)
        except:
            pass
    return unread_chats


# In[7]:


def findUnsavedContacts(unread_chats):
    # FILTRA CONTATOS NAO SALVOS DAS CONVERSAS NAO LIDAS
    unsaved_contact = []
    for chat in unread_chats:
        chat_title = chat.find_element_by_class_name('_19RFN').text
        if chat_title.startswith('+'):
            unsaved_contact.append(chat)
    return unsaved_contact if unsaved_contact != [] else False


# In[8]:


def verifyChats():
    '''
        Verifica se ha conversas para que o conteudo seja enviado
    '''
    unread_chats = findUnreadChats()
    return True if unread_chats != False and findUnsavedContacts(unread_chats) != False else False


# In[9]:


def verifyHistory():
    '''
        Verifica o historico da conversa se eh uma conversa nova ou nao
    '''
    
    engine_messages = ['Messages you send to this chat and calls are secured with end-to-end encryption. Click for more info.']
    
    history = driver.find_elements_by_class_name('FTBzM')
    
    for message in history:
        if message.text in engine_messages:
            return True
            #vai para uma conversa salva e encaminha as mensagens
    return False


# In[10]:


def selectChat(contact):
    '''
        Usando a caixa de pesquisa ira abrir uma conversa especifica
    '''
    try:
        #na caixa de pesquisa digita o nome do contato
        search_box = driver.find_element_by_class_name('_2zCfw')
        search_box.click()
        search_box.send_keys(contact)
        time.sleep(wait)
        
        #seleciona o contato
        for contact in driver.find_elements_by_class_name('_19RFN'):
            if contact.text == chat_name:
                time.sleep(2)
                contact.click()
                return True
    except Exception as error:
        print(type(error), error)
        return False


# In[11]:


def openMainChat():
    '''
        Abre a conversa principal onde esta o conteudo a ser encaminhado
    '''
    main_chat = 'DIVO'

    try:
        selectChat(main_chat)

        chats = driver.find_elements_by_class_name('KgevS')
        for chat in chats:
            if chat.find_element_by_class_name('_19RFN').get_attribute('title') == main_chat:
                chat.click()
                return True
    except Exception as error:
        print(type(error), error)
        return False


# In[12]:


def sendFirstMessages():
    '''
        Envia as primeiras mensagens de boas vindas
    '''
    message1 = 'Olá! Que bacana seu contato, amei!'
    message2 = 'Vou te explicar tudo ...'
    
    try:
        send_text_box = driver.find_element_by_class_name('_3u328')

        send_text_box.click()
        #envia a primeira mensagem
        send_text_box.send_keys(message1)
        time.sleep(1)
        send_text_box.send_keys(Keys.ENTER)

        #envia a segunda mensagem
        send_text_box.send_keys(message2)
        time.sleep(1)
        send_text_box.send_keys(Keys.ENTER)
        return True
    except Exception as error:
        print(type(error), error)
        return False


# In[13]:


def sendOtherMessages():
    '''
        Envia as primeiras mensagens de boas vindas
    '''
    messages = ['O mini ensaio é um sucesso no meu trabalho , oferecemos a mesma qualidade de todos os ensaios do meu catálogo. O diferencial é o valor é por ser mais enxuto , mas é lindo!',
               'E na edição desse ano, vem com revista Diva que é a queridinha do meu trabalho! Um revista com as suas melhores fotos e totalmente personalizada no seu estilo.',
                'O valor é imperdível e para que todas as mulheres possam viver essa experiência única!',
                'Qualquer dúvida me chama, vou amar conversar com vc!']
    
    try:
        for message in messages:
                send_text_box = driver.find_element_by_class_name('_3u328')

                send_text_box.click()
                #envia a primeira mensagem
                send_text_box.send_keys(message)
                time.sleep(3)
                send_text_box.send_keys(Keys.ENTER)
        return True
    except Exception as error:
        print(type(error), error)
        return False


# In[14]:


def sendAudioFile(contact_to_send):
    '''
        Encontra o arquivo de audio e passa para a funcao encaminhar
    '''
    messages = driver.find_elements_by_class_name('FTBzM')
    
    for message in messages:
        try:
            # se nao der erro eh pq a mensagem eh o audio
            message.find_element_by_class_name('_1N8Pv')
            if forwardContent(message, contact_to_send):
                return True
        except Exception as error:
    #         print(type(error), error)
            pass
    
    
    # se algo nao der certo ira retornar False
    return False

def sendVideo(contact_to_send):
    '''
        Encontra o video e passa para a funcao encaminhar
    '''
    # envia o video
    messages = driver.find_elements_by_class_name('FTBzM')
    for message in messages:
        try:
            message.find_element_by_class_name('_3Z-uK')
            if forwardContent(message, contact_to_send):
                return True
        except Exception as error:
    #         print(type(error), error)
            pass


# In[15]:


def sendImage(contact_to_send):
    '''
        Encontra o video e passa para a funcao encaminhar
    '''
    # envia o video
    messages = driver.find_elements_by_class_name('FTBzM')
    for message in messages:
        try:
            message.find_element_by_tag_name('img')
            if forwardContent(message, contact_to_send):
                return True
        except Exception as error:
#             print(type(error), error)
            pass
    return False


# In[16]:


def forwardContent(message, contact_to_send):
    '''
        recebe uma mensagem e clica no botao encaminhar entao seleciona o contato para o qual encaminhar
    '''
    try:
        message.find_element_by_class_name('gxf3C').click()

        #apos encontrar o audio ira enviar
        selectChat(contact_to_send)  
        time.sleep(2)

        #clica em enviar
        driver.find_element_by_class_name('_1g8sv').click()
        return True
    except Exception as error:
            print(type(error), error)
            return False


def saveTalked(chat_name):
    '''
        salva os contatos que ja foram atendidos
    '''
    with open('talked_chats.txt', 'a') as filee:
        filee.write(chat_name + '\n')
    return True

def verifyTalked(chat_name):
    '''
        Verifica se ja conversou com aquele contato antes
    '''
    with open('talked_chats.txt', 'r') as filee:
        talked = filee.read().split('\n')
    
    return True if chat_name in talked else False




# In[21]:


openBrowser('nomadbitcoin')


# In[ ]:


working = True
talked = []
report = []
wait = 5
while working:
    try:
        #verifica se ha conversas nao lidas com contatos nao salvos
        if verifyChats() and findUnsavedContacts(findUnreadChats()) != False:
            # se houver, ira clicar em cada um deles e verifica o historico 
            for unsaved_contact in findUnsavedContacts(findUnreadChats()):
                chat_name = unsaved_contact.find_element_by_class_name('_19RFN').text
                unsaved_contact.click()
                if verifyHistory() and not verifyTalked(chat_name):
                    #envia as primeiras mensagens
                    sendFirstMessages()
                    time.sleep(wait)
                    
                    #abre a conversa principal onde ha o conteudo a ser encaminhado e envia o audio
                    if openMainChat():
                        time.sleep(wait)
                        sendAudioFile(chat_name)
                        time.sleep(wait)
                    
                    if openMainChat():
                        time.sleep(wait)
                        sendVideo(chat_name)
                        time.sleep(wait)
                        
                    if openMainChat():
                        time.sleep(wait)
                        sendImage(chat_name)
                        time.sleep(wait)
                    
                    #envia as outras mensagens de texo
                    sendOtherMessages()
                    
                    #verifica se o audio foi vizualizado e entao encaminha o video
                    print('{} contato novo atendido - {}'.format(datetime.now().strftime('%d/%m/%y %H:%M:%S'), chat_name))
                    saveTalked(chat_name)
                    report.append({chat_name:datetime.now().strftime('%d/%m/%y %H:%M:%S')})
                    # working = False
                    
    except KeyboardInterrupt:
        do = input('Deseja parar o Autoatendimento? \nDigite 1 ou "sim" para parar, ou qualquer outra tecla para continuar\n:')
        if do == 'sim' or do == '1':
            print('parando...')
            working = False
        else:
            print('continuando....')
            pass


# In[ ]:


#adicionar um marcador
#enviar relatorio para carmen de quantas pessoas foram antendidas no dia

