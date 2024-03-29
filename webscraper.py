from bs4 import BeautifulSoup
import requests
import re
import json

url = 'https://cestina-pro-cizince.cz/obcanstvi/databanka-uloh/'

page = requests.get(url)

soup = BeautifulSoup(page.text, features="html.parser")
root = soup.find('div', class_ = "interaktivne") 
children = root.findChildren(recursive=False)
db = { 'sections' : []}
section_title=None
for child in children:    
    
    if child.name == 'h3':
        if child.next_element.next_element:
            section_title = child.next_element.next_element.text  
    if child.name == 'ol':
        section = { 'title' : section_title, 'questions':[]}
        questionid=0
        for li in child:
            q = {'id':None,'question':None, 'image':None, 'options':[], 'answer': None}

            title = li.find('div', class_ = "text")
            if title:
                q['id'] = questionid
                q['question'] = title.text

            img = li.find('img', class_ = "imgQ")
            if img:
                q['image'] = img['src']

            questions = li.find('ol', class_ = "alternatives")
            for question in questions:
                tabvarimg = question.find('div', class_ = 'tabvar tabvarimg container')
                if tabvarimg:
                    img_options = tabvarimg.find_all('div', class_ = 'imgAltWrapper', recursive=True)
                    for img_option in img_options:                      

                        img_lable = img_option.find('label')
                        if img_lable:
                           
                            if img_lable:
                                option = {'id':None, 'text': None, 'image':None}
                                                        
                                if img_lable.text:
                                    option['text'] = img_lable.text
                                    option['id'] = re.search(r'\b([A-Za-z])', img_lable.text).group(1)

                                img = img_lable.find('img')
                                if img:
                                    option['image'] = img['src']

                                q['options'].append(option)
                else:                          
                    label = question.find('label')
                    option = {'text': None}
                    if label:
                        
                        if label.text:
                            option['text'] = label.text
                            option['id'] = re.search(r'\b([A-Za-z])', label.text).group(1)
                        q['options'].append(option)
                    elif question.attrs['class'][0] == 'spravnaOdpoved':
                        span = li.find('span', class_ = "spravne")
                        q['answer'] = re.search(r'\b([A-Za-z])\b', span.text).group(1) 

            section['questions'].append(q)
            questionid = questionid + 1

        db['sections'].append(section)

with open('Q&A.json', 'w', encoding='utf-8') as json_file:
    json.dump(db, json_file,ensure_ascii=False)
