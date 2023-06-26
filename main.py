from reactpy import component,html,hooks   
from reactpy.backend.fastapi import  configure
from fastapi import FastAPI

import requests


@component
def Item(text, initial_done=False):

    


   

    done, set_done = hooks.use_state(initial_done)

    def handle_click(event):
      set_done(not done)
      
     
    attr= {"style": {"color": "green"}} if done else {"style": {"color": "red"}}


    if done:
       return html.li(attr, text)
    else:
       return html.li(
          html.span(attr, text),
          html.button({ "on_click": handle_click }," Fet!")


       )


@component
def Todos(items): 
   
   choices, set_choices = hooks.use_state([])
   resposta, set_resposta = hooks.use_state("")


   #valor=""

   def handle_choices(event):
      set_resposta("Gràcies per la teva resposta")

   def handle_click(event):
      id = event['target']['value']
      # obtenim llista de choices

      choices_API = requests.get('http://localhost:8002/api/get_choices/'+id)

      resultat = choices_API.json()


      print (resultat)

      items_choices= resultat['choices']



      set_choices( [
        html.option( { "value":i['id']},i['choice_text'])
        #html.button({"on_click": handle_click, "value":i['id'] }," Fet!")
        for i in items_choices
      ])



   list_item_elements = [
    

      #html.select(
      html.option( { "value":i['id']},i['question_text'])
      #html.button({"on_click": handle_click, "value":i['id'] }," Fet!")
      for i in items

   ]
   return html.div (
     html.select({"on_change": handle_click },list_item_elements),
     html.select({"on_change": handle_choices },choices),
     html.div(resposta)
   ) 


  

@component
def HelloWorld():
    
    #response_API = requests.get('https://jsonplaceholder.typicode.com/todos/')
    response_API = requests.get('http://localhost:8002/api/get_questions')


    resultat = response_API.json()
    questions =  resultat['questions']
    # for parcial in resultat:
    #    print(parcial['question_text'])
    for parcial in questions:
        print(parcial['question_text'])

      
    


    return html._(
      html.h1("Llista de tasques ! "),
      html.div(Todos(questions)),

      html.ul(
        Item("Aprendre React amb Python", True),
        Item("Dominar Django com un pro"),
        Item("Sobreviure a un projecte amb Laravel")
        
      )
    )



app = FastAPI()
configure (app, HelloWorld )
 

