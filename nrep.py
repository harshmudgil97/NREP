#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 23:16:40 2019

Non Regenerative Email Processor prototype version 0.2

NREP p -v0.2

@author: harsh
"""

import bs4 as bs
import nltk
import re
import os
import time
import imaplib
import email


from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


mail = imaplib.IMAP4_SSL('imap.gmail.com')
clear = lambda: os.system('clear')

stop_words = nltk.corpus.stopwords.words('english')


def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)

def clean_text(text):

    text = re.sub(r'donâ€™t','do not', text)
    text = re.sub(r'\[[0-9]*\]',' ',text)
    text = re.sub(r'thanks','',text)
    text = re.sub(r'Thanks','',text)
    text = re.sub(r'Regards','',text)
    text = re.sub(r'regards','',text)
    text = re.sub(r'thanking','',text)
    text = re.sub(r'Thanking','',text)
    text = re.sub(r'Yours faithfully','',text)
    text = re.sub(r'Yours sincerely','',text)
    text = re.sub(r'Yours faithfully','',text)
    text = re.sub(r'Yours truly','',text)
    text = re.sub(r'Dear','',text)
    text = re.sub(r'dear','',text)
    text = re.sub(r'Sir','',text)
    text = re.sub(r'sir','',text)


    text = re.sub(r'\s+',' ',text)
    text = re.sub(r'^\s','',text)




    return text

def send_mail(name):
    clear()
    print("\n\nFeature Coming Soon\n\n")
    contacts_disp()


def dispLexSummary(text):
    s = nltk.sent_tokenize(text)
    k = s[1:len(s)-1]
    n = []
    n.append(k)
    for i in range(len(n)):
        te = ' '.join(n[i])



    #Summarize the document with 2 sentences
    parser = PlaintextParser.from_string(te,Tokenizer("english"))

    summarizer = LexRankSummarizer()
    #Summarize the document with 2 sentences
    summary = summarizer(parser.document,3 )
    t = ''
    for sentence in summary:
        s = re.sub(r'\n',' ',str(sentence))
        t+=s
    print(t)



def view_messages(list_ids):
    clear()
    time.sleep(1)
    print('................Loading messages.................\n\n')
    time.sleep(2)
    clear()
    for item in list_ids:
        res,data = mail.uid('fetch',item,'(RFC822)')
        e_mail = email.message_from_bytes(data[0][1])
        soup = bs.BeautifulSoup(get_body(e_mail),'html.parser')
        text = soup.get_text()

        text = clean_text(text)
        dispLexSummary(text)


        print('\n....................................................\n')

    time.sleep(2)
    f = input('Enter \'yes\' to go back to main menu: ')
    if f =='yes':
        contacts_disp()
    else:
        clear()
        print("\n..........INVALID RESPONSE. TRY AGAIN..........\n")
        view_messages(list_ids)


def contacts_disp():
    time.sleep(1)
    clear()
    mail.select('Inbox')
    res,data = mail.uid('search',None,'ALL')
    inbox_item_list = data[0].split()

    e_dict={}
    for item in inbox_item_list:
        res,data = mail.uid('fetch',item,'(RFC822)')
        raw_mail = data[0][1].decode('utf-8')
        e_mail = email.message_from_string(raw_mail)
        sender = e_mail['From']
        sender = re.sub(r'\<[^)]*\>', '', sender)
        sender = re.sub(r'^\s','',sender)
        sender = re.sub(r'\s$','',sender)
        list_if = []
        list_if.append(item)
        if sender.lower() in e_dict.keys():
            e_dict[sender.lower()].append(item)
        else:
            e_dict[sender.lower()] = list_if


    print("\nAvailable messages from / contacts......: \n")
    for i in e_dict.keys():
        time.sleep(1)
        print(i + '\n')

    s_name = input('Type in contact name to see/send messages: ')

    if s_name.lower() in e_dict.keys():
        v_opt = input('Type see or send to select the respective option: ')
        if v_opt.lower() == 'see':
            list_ids = []
            for i in e_dict.keys():
                if s_name == i:
                    list_ids = [j for j in e_dict[i]]
            view_messages(list_ids)

        elif v_opt.lower() == 'send':
            send_mail(s_name)

        else:
            clear()
            print("\n\n\n........INVALID RESPONSE..........\n\n\n")
            time.sleep(2)
            contacts_disp()
    else:
         clear()
         print("\n\n\n........INVALID RESPONSE..........\n\n\n")
         time.sleep(2)
         contacts_disp()



def log_in(u_name,p_word):
    res,co = mail.login(u_name,p_word)
    if res == 'OK':
        clear()
        print('\nLOGIN SUCCESSFUL.\n\n....Pls Wait Loading Contacts....\n')
        time.sleep(1)
        contacts_disp()
    else:
        clear()
        print("\n..........INVALID EMAIL OR PASSWORD. TRY AGAIN..........\n")
        main()

def main():
    userName = input('Enter Email Address: ')
    passWord = input('Enter Password: ')
    log_in(userName,passWord)

if __name__ == '__main__':
    main()
