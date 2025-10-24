import pandas as pd
import random
import uuid

# Extended lists of simple phrases for each language
phrases_uk = [
    "Привіт, як справи?", "Де найближча аптека?", "Як налаштувати Wi-Fi?", "Мені потрібна допомога!",
    "Скільки коштує квиток?", "Що таке штучний інтелект?", "Дякую за вашу увагу.",
    "Як дістатися до вокзалу?", "Чи є вільні місця в ресторані?", "Це терміново, викличте лікаря!",
    "Як підключити принтер до комп'ютера?", "Чи можу я замовити таксі?", "Який сьогодні курс валют?",
    "Будь ласка, поясніть це ще раз.", "Як працює ця програма?", "Де я можу купити квитки на концерт?",
    "Чи є у вас вегетаріанське меню?", "Мені потрібен переклад цього документа.",
    "Як довго триватиме ремонт?", "Чи можу я повернути цей товар?", "Який час зараз?",
    "Де знаходиться бібліотека?", "Скільки коштує ця книга?", "Чи можу я спробувати це?",
    "Як звати вашого собаку?", "Мені подобається це місце.", "Чи йде дощ?", "Де мій телефон?",
    "Я хочу чашку кави.", "Чи є тут парковка?", "Як далеко до аеропорту?", "Це смачно!",
    "Чи можу я оплатити карткою?", "Який у вас пароль Wi-Fi?", "Мені холодно.",
    "Де я можу знайти готель?", "Скільки це коштує?", "Чи є у вас знижки?",
    "Я загубив свої ключі.", "Як зв’язатися з підтримкою?", "Чи можу я взяти це з собою?"
]

phrases_en = [
    "Hello, how are you?", "Where is the nearest pharmacy?", "How to set up Wi-Fi?", "I need help!",
    "How much is the ticket?", "What is artificial intelligence?", "Thank you for your attention.",
    "How to get to the train station?", "Are there free seats in the restaurant?", "It's urgent, call a doctor!",
    "How to connect a printer to the computer?", "Can I order a taxi?", "What is today's exchange rate?",
    "Please explain it again.", "How does this program work?", "Where can I buy concert tickets?",
    "Do you have a vegetarian menu?", "I need a translation of this document.",
    "How long will the repair take?", "Can I return this item?", "What time is it now?",
    "Where is the library?", "How much is this book?", "Can I try this on?",
    "What is your dog's name?", "I like this place.", "Is it raining?", "Where is my phone?",
    "I want a cup of coffee.", "Is there parking here?", "How far is the airport?", "This is delicious!",
    "Can I pay by card?", "What is your Wi-Fi password?", "I'm cold.",
    "Where can I find a hotel?", "How much does it cost?", "Do you have any discounts?",
    "I lost my keys.", "How do I contact support?", "Can I take this to go?"
]

phrases_es = [
    "¡Hola, cómo estás?", "¿Dónde está la farmacia más cercana?", "¿Cómo configurar Wi-Fi?", "¡Necesito ayuda!",
    "¿Cuánto cuesta el boleto?", "¿Qué es la inteligencia artificial?", "Gracias por su atención.",
    "¿Cómo llegar a la estación de tren?", "¿Hay asientos libres en el restaurante?", "¡Es urgente, llame a un médico!",
    "¿Cómo conectar una impresora a la computadora?", "¿Puedo pedir un taxi?", "¿Cuál es el tipo de cambio hoy?",
    "Por favor, explícalo de nuevo.", "¿Cómo funciona este programa?", "¿Dónde puedo comprar entradas para un concierto?",
    "¿Tienen menú vegetariano?", "Necesito una traducción de este documento.",
    "¿Cuánto tiempo tomará la reparación?", "¿Puedo devolver este artículo?", "¿Qué hora es ahora?",
    "¿Dónde está la biblioteca?", "¿Cuánto cuesta este libro?", "¿Puedo probarme esto?",
    "¿Cómo se llama tu perro?", "Me gusta este lugar.", "¿Está lloviendo?", "¿Dónde está mi teléfono?",
    "Quiero una taza de café.", "¿Hay estacionamiento aquí?", "¿A qué distancia está el aeropuerto?", "¡Esto es delicioso!",
    "¿Puedo pagar con tarjeta?", "¿Cuál es la contraseña del Wi-Fi?", "Tengo frío.",
    "¿Dónde puedo encontrar un hotel?", "¿Cuánto cuesta?", "¿Tienen descuentos?",
    "Perdí mis llaves.", "¿Cómo contacto con soporte?", "¿Puedo llevar esto para llevar?"
]

phrases_fr = [
    "Bonjour, comment vas-tu ?", "Où est la pharmacie la plus proche ?", "Comment configurer le Wi-Fi ?", "J'ai besoin d'aide !",
    "Combien coûte le billet ?", "Qu'est-ce que l'intelligence artificielle ?", "Merci pour votre attention.",
    "Comment aller à la gare ?", "Y a-t-il des places libres au restaurant ?", "C'est urgent, appelez un médecin !",
    "Comment connecter une imprimante à l'ordinateur ?", "Puis-je commander un taxi ?", "Quel est le taux de change aujourd'hui ?",
    "S'il vous plaît, expliquez encore.", "Comment fonctionne ce programme ?", "Où puis-je acheter des billets pour un concert ?",
    "Avez-vous un menu végétarien ?", "J'ai besoin d'une traduction de ce document.",
    "Combien de temps prendra la réparation ?", "Puis-je retourner cet article ?", "Quelle heure est-il maintenant ?",
    "Où est la bibliothèque ?", "Combien coûte ce livre ?", "Puis-je essayer ceci ?",
    "Comment s'appelle votre chien ?", "J'aime cet endroit.", "Est-ce qu'il pleut ?", "Où est mon téléphone ?",
    "Je veux une tasse de café.", "Y a-t-il un parking ici ?", "À quelle distance est l'aéroport ?", "C'est délicieux !",
    "Puis-je payer par carte ?", "Quel est le mot de passe Wi-Fi ?", "J'ai froid.",
    "Où puis-je trouver un hôtel ?", "Combien ça coûte ?", "Avez-vous des réductions ?",
    "J'ai perdu mes clés.", "Comment contacter le support ?", "Puis-je emporter ceci ?"
]

# Translation dictionary
translations = {
    'uk': {
        'en': lambda x: phrases_en[phrases_uk.index(x)] if x in phrases_uk else x,
        'es': lambda x: phrases_es[phrases_uk.index(x)] if x in phrases_uk else x,
        'fr': lambda x: phrases_fr[phrases_uk.index(x)] if x in phrases_uk else x
    },
    'en': {
        'uk': lambda x: phrases_uk[phrases_en.index(x)] if x in phrases_en else x,
        'es': lambda x: phrases_es[phrases_en.index(x)] if x in phrases_en else x,
        'fr': lambda x: phrases_fr[phrases_en.index(x)] if x in phrases_en else x
    },
    'es': {
        'uk': lambda x: phrases_uk[phrases_es.index(x)] if x in phrases_es else x,
        'en': lambda x: phrases_en[phrases_es.index(x)] if x in phrases_es else x,
        'fr': lambda x: phrases_fr[phrases_es.index(x)] if x in phrases_es else x
    },
    'fr': {
        'uk': lambda x: phrases_uk[phrases_fr.index(x)] if x in phrases_fr else x,
        'en': lambda x: phrases_en[phrases_fr.index(x)] if x in phrases_fr else x,
        'es': lambda x: phrases_es[phrases_fr.index(x)] if x in phrases_fr else x
    }
}

# Settings
languages = ['uk', 'en', 'es', 'fr']
contexts = ['Casual', 'Formal', 'Technical', 'Travel', 'Emergency']
intents = ['Translate', 'Request', 'Inform', 'Clarify']
sentence_lengths = ['Short', 'Medium', 'Long']

# Generate 1500 rows
data = []
for i in range(1500):
    input_lang = random.choice(languages)
    target_lang = random.choice([l for l in languages if l != input_lang])
    context = random.choices(contexts, weights=[0.2, 0.2, 0.2, 0.2, 0.2], k=1)[0]
    intent = random.choices(intents, weights=[0.4, 0.3, 0.2, 0.1], k=1)[0]

    # Select phrase
    if input_lang == 'uk':
        input_text = random.choice(phrases_uk)
    elif input_lang == 'en':
        input_text = random.choice(phrases_en)
    elif input_lang == 'es':
        input_text = random.choice(phrases_es)
    else:
        input_text = random.choice(phrases_fr)

    # Translate
    translated_text = translations[input_lang][target_lang](input_text)

    # Sentence length
    word_count = len(input_text.split())
    if word_count < 5:
        sent_len = 'Short'
    elif word_count <= 10:
        sent_len = 'Medium'
    else:
        sent_len = 'Long'

    data.append({
        'ID': i + 1,
        'Input_Text': input_text,
        'Input_Language': input_lang,
        'Target_Language': target_lang,
        'Translated_Text': translated_text,
        'Context': context,
        'Sentence_Length': sent_len,
        'Intent': intent
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('speech_translator_dataset_1500.csv', index=False)

# Display first 10 rows
print(df.head(10))