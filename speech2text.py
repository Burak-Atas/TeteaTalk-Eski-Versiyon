
import os
from unicodedata import name
from urllib import response
from google.cloud import texttospeech_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\softw\\Desktop\\GoogleAPIdemo\\zeta-yen-380821-da5ad3c0bbd0.json"


#yeni bir nesne oluşturduk


def text2speech(client , userid, input):

    #seslendirmek istediğimiz deişken
    text = '<speak>'+input+'</speak>'

    #seslendirmek istediğimiz metin
    synthesis_input = texttospeech_v1.SynthesisInput(ssml=text)


    #ses yapılandırması
    voice1 = texttospeech_v1.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech_v1.SsmlVoiceGender.MALE,
        name='en-US-Neural2-I'

    )

    #mevcut sesler
    print(client.list_voices)

    #ses hızı kodlama frekansı
    audio_config = texttospeech_v1.AudioConfig(
        speaking_rate=0.9,
        audio_encoding = texttospeech_v1.AudioEncoding.MP3
    )

    response1 = client.synthesize_speech(
        input=synthesis_input,
        voice=voice1,
        audio_config=audio_config
    )

    
    directory = "static/" + userid

    file = "static/"+userid+"/audio.mp3"
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file, 'wb') as output:
        output.write(response1.audio_content)