from selenium import webdriver
import time
from datetime import datetime, date, timedelta 

class history_messages():
    def __init__(self, driver):
        self.driver = driver

    # VERIFICA SE EH O FIM DA CONVERSA
    def verify_end(self):
        engine_messages = ['As mensagens e chamadas dessa conversa estão protegidas com criptografia de ponta a ponta.', 'As mensagens e chamadas dessa conversa estão protegidas com criptografia de ponta a ponta. iFood pode contratar outra empresa para armazenar, ler e responder às suas mensagens e chamadas. Clique para mais informações.',
                        'As mensagens e as chamadas dessa conversa são protegidas com a criptografia de ponta a ponta. Clique para mais informações.']
        try:
            if self.driver.find_elements_by_xpath('//div[@role="button"]')[9].text in engine_messages:
                return True
            else:
                return False
        except:
            return False
        
    def scroll_history(self):
        #se nao for o fim da conversa, ira dar scroll para cima
        run = True
        while run: 
            if not self.verify_end():
                try:
                    div_chat = self.driver.find_element_by_class_name('_1ays2')
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", div_chat)
                    time.sleep(0.3)
                except Exception as error:
                    print(type(error), error)
                    return False
            else:
                run = False
        return True
    
    
    # FUNCOES QUE LIDAM COM O SCROLL UP DAS CONVERSAS PARA CAPUTRAR TODO O HISTORICO
    def block_time(self, mensagem):
        days_week = ['TODAY', 'YESTERDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 
                    'HOJE', 'ONTEM', 'SEGUNDA-FEIRA', 'TERÇA-FEIRA', 'QUARTA-FEIRA', 'QUINTA-FEIRA', 'SEXTA-FEIRA', 'SÁBADO', 'DOMINGO']
        try:
            content = mensagem.text
            if len(content) == 10 and content[2] == '/' and content[5] == '/':
                return content
            elif content in days_week:
                #chama funcao que vai tratar o dia da semana e devolver uma data
                content = self.correct_day(content)
                return content
            else:
                return False
        except Exception as error:
            print(' ___ >>> block_time <<< ___ [function: block_time()]')
            print(type(error), error)
            return False
        
    #CORRIGE O DIA DA SEMANA CASO NAO SEJA UMA DATA ESPECIFICA
    def correct_day(self, day_name):
        #traduz o dia da semana caso o whatsapp esteja em portugues
        d = date.today()
        
        days_pt = {'SEGUNDA-FEIRA': 'monday', 'TERÇA-FEIRA': 'tuesday', 'QUARTA-FEIRA': 'wednesday', 'QUINTA-FEIRA': 'thursday', 'SEXTA-FEIRA': 'friday', 'SÁBADO': 'saturday', 'DOMINGO': 'sunday', 'HOJE': 'TODAY', 'ONTEM': 'YESTERDAY'}
        if day_name in days_pt.keys():
            day_name = days_pt[day_name]
        
        if day_name == 'TODAY':
            corrected = date.today()
            return corrected.strftime('%d/%m/%Y')
        elif day_name == 'YESTERDAY':
            corrected = d + timedelta(days=-1)
            return corrected.strftime('%d/%m/%Y')
        
        days_of_week = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        target_day = days_of_week.index(day_name.lower())
        delta_day = target_day - d.isoweekday()
        
        if delta_day >= 0: delta_day -= 7 # go back 7 days
        corrected = d + timedelta(days=delta_day)
        return corrected.strftime('%d/%m/%Y')

    # FUNCOES PARA TRATAR CADA MENSAGEM, TIME, STATUS, SE FOI ENVIADA OU RECEBIDA E CONTEUDO
    def get_time(self, mensagem):
        #verifica o horario da mensagem
        #pega o tempo de cada mensagem
        try:
            time = mensagem.find_element_by_css_selector('span._3fnHB').text
            return time
        except:
            return 'ENGINE'
            pass

    def get_source_status(self, mensagem, time):
        #verifica se eh mensagem recebida ou enviada
        #se for enviada verifica o status
        try:
            status = mensagem.find_element_by_css_selector('path').get_attribute('fill') 
            if status == 'FFF':
                return 'sent'
            elif status == '92A58C':
                return 'delivered'
            else:
                return 'viewed'
        except:
            #se nao tiver icone de status e nao for o balao de data do whatsapp, eh mensagem recebida
            if time != 'ENGINE':
                return 'received'
            else:
                #criar metodo que ira organizar as mensagens em um bloco de tempo
                return 'ENGINE'

    def verify_content(self, mensagem):
        #verifica qual o conteudo da mensagem
        content = {'content': '', 'type': ''}
        
        #verifica se eh um audio
        try:
            audio = mensagem.find_element_by_css_selector('audio').get_attribute('src')
            content['content'] = 'audio: ' + str(audio)
            content['type'] = 'audio'
        except:
            #verifica se eh umagem
            try:
                link = mensagem.find_element_by_css_selector('img').get_attribute('src')
                content['content'] = link
                content['type'] = 'image'
            except:
                try:
                    video = mensagem.find_element_by_class_name('_3_IKd')
                    content['content'] = 'duracao do video: ' + str(video.text)
                    content['type'] = 'video'
                except:
                    #se nao for imagem nem video nem audio eh texto, se for documento pegara o nome do arquivo
                    try:
                        content_msg = mensagem.text.split('\n')
                        
                        if '#NaBike' in content_msg:
                            content['content'] = '|'.join(content_msg)
                            content['type'] = 'automatic'
                        elif len(content_msg) > 2 and content[0].startswith('+55') and content[2].startswith('+55') :
                            content['content'] = '|'.join(content_msg)
                            content['type'] = 'replie'
                        else:
                            #verifica se eh mensagem deletada
                            try:
                                mensagem.find_element_by_class_name('-bh0C')
                                content['content'] = 'This message was deleted'
                                content['type'] = 'deleted'
                            except:
                                #se nao for nenhuma das possibilidaes anteriores, eh texto
                                lengh = mensagem.text.split('\n')
                                if len(lengh) > 1:
                                    content['content'] = str(mensagem.text)
                                    content['type'] = 'text'
                                else:
                                    content['content'] = lengh[0]
                                    content['type'] = 'text'
                    except:
                        try:
                            lengh = mensagem.text.split('\n')
                            if len(lengh) > 1:
                                content['content'] = str(mensagem.text)
                                content['type'] = 'text'
                            else:
                                content['content'] = lengh[0]
                                content['type'] = 'text'
                        except Exception as error:
                            print(error)
                            content['content'] = 'desconhecido'
                            content['type'] = 'unknown'  
        return content


    # In[10]:


    # PEGA O CONTEUDO DAS MENSAGENS E DO CONTATO
    def getContent(self, need_scroll=True):
        try:
            if need_scroll == True:
                self.scroll_history()
            
            div_chat = self.driver.find_element_by_class_name('_1ays2')
            mensagens = div_chat.find_elements_by_class_name('FTBzM')

            history = {}
            
            timeline = []
            date = 'no date'
            
            for msg in mensagens:
                message = {'status': None, 'time': None, 'content': None, 'type': None}
                
                #pega o tempo de cada mensagem
                message['time'] = self.get_time(msg)
                
                #verifica se eh mensagem enviada ou recebida, se a mensagem nao tiver tempo eh o balao com a data
                message['status'] = self.get_source_status(msg, message['time'])
                
                content = self.verify_content(msg)
                
                message['type'] = content['type']
                message['content'] = content['content']
                
                is_time = self.block_time(msg)
                if is_time != False:
                    #se for tempo, cria um dicionario que armazena o a lista de dicionarios com dados de cada mensagem
                    date = is_time
                    timeline.append({date: []})
                else:
                    #adiciona o dicionario de dados na lista que ja existe
                    try:
                        timeline[-1][date].append(message)
                    except IndexError:
                        timeline.append({date: []})
                        timeline[-1][date].append(message)
                
            return timeline
        except Exception as error:
            assert 'NoSuchElementException' not in str(type(error)), 'Nenhum chat aberto'
            print(type(error), error)