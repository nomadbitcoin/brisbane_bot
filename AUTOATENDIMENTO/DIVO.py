#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import platform
from datetime import datetime
from sys import stdout
import history


# In[2]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys


# In[3]:


wait = 3


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


# In[5]:


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


# In[6]:


def findUnsavedContacts(unread_chats):
    # FILTRA CONTATOS NAO SALVOS DAS CONVERSAS NAO LIDAS E VERIFICA SE JA CONVERSOU
    unsaved_contact = []
    for chat in unread_chats:
        chat_title = chat.find_element_by_class_name('_19RFN').text
        if chat_title.startswith('+') and not verifyTalked(chat_title):
#             unsaved_contact.append(chat)
            return chat
    return False


# In[7]:


def verifyChats():
    '''
        Verifica se ha conversas para que o conteudo seja enviado
    '''
    unread_chats = findUnreadChats()
    return True if unread_chats != False and findUnsavedContacts(unread_chats) != False else False


# In[8]:


def verifyHistory(unsaved_contact):
    '''
        Verifica o historico da conversa se eh uma conversa nova ou nao
    '''
    unsaved_contact.click()
    engine_messages = ['Messages you send to this chat and calls are secured with end-to-end encryption. Click for more info.',
                      'As mensagens e as chamadas dessa conversa são protegidas com a criptografia de ponta a ponta. Clique para mais informações.']
    
    history = driver.find_elements_by_class_name('FTBzM')
    
    for message in history:
        if message.text in engine_messages:
            return True
            #vai para uma conversa salva e encaminha as mensagens
    return False


# In[9]:


def selectChat(contact):
    '''
        Usando a caixa de pesquisa ira abrir uma conversa especifica
    '''
    try:
        #na caixa de pesquisa digita o nome do contato
        search_box = driver.find_element_by_class_name('_2zCfw')
        search_box.click()
        search_box.send_keys(Keys.CONTROL + 'a')
        search_box.send_keys(Keys.BACKSPACE)
        search_box.send_keys(contact)
        time.sleep(wait)
        
        #talvez isso aqui possa dar pau, verificar
        chat_name = contact
        
        #seleciona o contato
        for contact in driver.find_elements_by_class_name('_19RFN'):
            if contact.text == chat_name:
                time.sleep(2)
                contact.click()
                return True
    except Exception as error:
        print(type(error), error)
        return False


# In[10]:


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


# In[11]:


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


# In[12]:


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


# In[13]:


def sendRemarketingMessages(message_type):
    '''
        Envia mensagens de remarketing, ha tipos de contatos possiveis:
        
        1 - Nao respondeu nenhuma vez,  
    '''
    type_1 = 'Seu feedback é muito importante para mim. O que achou da nossa proposta? Ficou fora da sua expectativa, ainda tem dúvidas, etc? Poderíamos agendar um horário para conversarmos? O que acha da ideia?'
    
    try:
        if message_type == 1:
            send_text_box = driver.find_element_by_class_name('_3u328')

            send_text_box.click()
            #envia a primeira mensagem
            send_text_box.send_keys(type_1)
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


# In[17]:


def saveTalked(chat_name, step):
    '''
        salva os contatos que ja foram atendidos
    '''
    if step == 1:
        #salva os contatos com os quais ja falou/fez o antendimento
        with open('talked_chats.txt', 'a') as filee:
            filee.write(chat_name + '\n')
        return True
    elif step == 2:
        #salva os contatos que ja fez o remarketing
        with open('remarketed.txt', 'a') as filee:
            filee.write(chat_name + '\n')
        return True
    elif step == 3:
        #salva os contatos que ja verificou se precisam de remarketing
        with open('remarket_verified.txt', 'a') as filee:
            filee.write(chat_name + '\n')
        return True
    
def verifyTalked(chat_name=None, get_list=False):
    '''
        Verifica se ja conversou com aquele contato antes
    '''
    with open('talked_chats.txt', 'r') as filee:
        talked = filee.read().split('\n')
    
    if chat_name != None:
        return True if chat_name in talked else False
    elif get_list != False:
        return talked


# In[18]:


def verifyRemarketed(step):
    '''
        Devolve a lista de contatos que ja foram feitos remarketing
    '''
    if step == 1:
        #devolve a lista dos que foi feito remarketing
        with open('remarketed.txt', 'r') as filee:
             remarketed_list = filee.read().split('\n')
        return remarketed_list
    elif step == 2:
        #devolve a lista dos que ja foi verificado se precisa de remarketing
        with open('remarket_verified.txt', 'r') as filee:
             remarket_verified = filee.read().split('\n')
        return remarket_verified


# In[19]:


def responseNewClients():
    try:
        #verifica se ha conversas nao lidas com contatos nao salvos
        unsaved_contact = findUnsavedContacts(findUnreadChats())
        if verifyChats() and unsaved_contact != False:
            # se houver, ira clicar em cada um deles e verifica o historico 
            chat_name = unsaved_contact.find_element_by_class_name('_19RFN').text

            if not verifyTalked(chat_name) and verifyHistory(unsaved_contact):
                time.sleep(wait)
                #envia as primeiras mensagens
                sendFirstMessages()
                time.sleep(wait)

                #abre a conversa principal onde ha o conteudo a ser encaminhado e envia o audio
                if openMainChat():
                    time.sleep(wait)
                    sendAudioFile(chat_name)
                    time.sleep(20)

                if openMainChat():
                    time.sleep(wait)
                    sendVideo(chat_name)
                    time.sleep(30)

                if openMainChat():
                    time.sleep(wait)
                    sendImage(chat_name)
                    time.sleep(10)

                #envia as outras mensagens de texo
                sendOtherMessages()

                #verifica se o audio foi vizualizado e entao encaminha o video
                print('contato novo atendido - {}'.format(chat_name))
                saveTalked(chat_name, 1)
#                 report.append({chat_name:datetime.now().strftime('%d/%m/%y %H:%M:%S')})
                return True
        return True            
    except KeyboardInterrupt:
        do = input('\n\nDeseja parar o Autoatendimento? \nDigite 1 ou "sim" para parar, ou qualquer outra tecla para continuar\n:')
        if do == 'sim' or do == '1':
            return False
    except Exception as error:
        print(type(error), error)
        return False


# In[20]:


def verifyNeedRemarketing():
    '''
        Ira verificar o historico e verificar se deve ser mandado a mensagem de remarketin
    '''
    received = 0
    messages_to_revise = messagesToRevise()
    if messages_to_revise != None:
        for message in messages_to_revise:
            if message['status'] == 'received':
                received +=1
        if received <=0:
            return True, 1
        else:
            return False, 0

def messagesToRevise():
    '''
        Ira encontrar a ultima mensagem enviada pelo bot e retornar o que ha dali em diante
    '''
    history_functions = history.history_messages(driver)
    full_history = history_functions.getContent(need_scroll=False)
    
    for days in full_history:
        for day in days.keys():
            messages = days[day]
            for num, message in enumerate(messages):
                if 'Qualquer dúvida me chama, vou amar conversar com vc!' in message['content']:
                    #se encontrar a ultima mensagem pelo bot ira salvar o que tiver dali pra frente para verificar
                    return messages[num:]
    return None


# In[27]:


# ABRIR A CONVERSA COM TODOS QUE JA FALOU E VERIFICAR SE FOI RESPONDIDO
def verifyNewClients():
    talked = verifyTalked(get_list=True)
    remarketed = verifyRemarketed(1)
    verified_remarket = verifyRemarketed(2)
    
    try:
        for contact_talked in talked:
            if contact_talked not in verified_remarket and contact_talked not in remarketed:
                
                selectChat(contact_talked)
            
                contact_verified = verifyNeedRemarketing()
                
                if contact_verified != None and contact_verified[0] == True: 
                    #primeiro item da lista eh True ou False e o segundo item eh o tipo de mensagem a ser enviada
                    sendRemarketingMessages(contact_verified[1])
                    print('remarketing enviado para: {}'.format(contact_talked))
                    saveTalked(contact_talked, 2)
                else:
                    saveTalked(contact_talked, 3)
                
        return True
    except KeyboardInterrupt:
        do = input('\n\nDeseja parar o Remarketing? \nDigite 1 ou "sim" para parar, ou qualquer outra tecla para continuar\n:')
        if do == 'sim' or do == '1':
            return False
    except Exception as error:
        print('\nError ___ >>> Remarketing <<< ___ [function: verifyNewClients()]\n')
        print(type(error), error)
        return False


# In[28]:


openBrowser('carmenkussler')


# In[ ]:


working = True
while working:
    # stdout.write('\r conferindo se está tudo ok... \n')
    if not responseNewClients():
        print('\nStopped ___ >>> Responder Novos Clientes <<< ___ [function: responseNewClients()]')
        working = False

#     stdout.write('\r Novos Clientes ok! \n')
#     if not verifyNewClients():
#         print('\nStopped ___ >>> Remarketing <<< ___ [function: verifyNewClients()]')
#         working = False
# #     stdout.write('\r Remarketing ok! \n')


# In[ ]:





# In[24]:


# SALVAR DATA DE QUANDO FALOU COM O CONTATO E VERIFICAR APOS DOIS DIAS SE EH NECESSARIO FAZER REMARKETING


# In[25]:


#adicionar um marcador
#enviar relatorio para carmen de quantas pessoas foram antendidas no dia

