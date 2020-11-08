import speech_recognition as sr
from gtts import gTTS
import playsound
from textblob import TextBlob

languages = ["afrikaans", "albanian", "amharic", "arabic", "armenian", "azerbaijani", "basque", "belarusian", "bengali",
             "bosnian", "bulgarian", "catalan", "cebuano", "chinese", "corsican", "croatian", "czech", "danish",
             "dutch", "english", "esperanto", "estonian", "finnish", "french", "frisian", "galician", "georgian",
             "german", "greek", "gujarati", "haitian creole", "hausa", "hawaiian", "hebrew", "hindi", "hmong",
             "hungarian", "icelandic", "igbo", "indonesian", "irish", "italian", "japanese", "javanese", "kannada",
             "kazakh", "khmer", "kinyarwanda", "korean", "kurdish", "kyrgyz", "lao", "latin", "latvian", "lithuanian",
             "luxembourgish", "macedonian", "malagasy", "malay", "malayalam", "maltese", "maori", "marathi",
             "mongolian", "myanmar", "nepali", "norwegian", "nyanja", "odia", "pashto", "persian", "polish",
             "portuguese", "punjabi", "romanian", "russian", "samoan", "scots gaelic", "serbian", "sesotho", "shona",
             "sindhi", "sinhala", "slovak", "slovenian", "somali", "spanish", "sundanese", "swahili", "swedish",
             "tagalog", "tajik", "tamil", "tatar", "telugu", "thai", "turkish", "turkmen", "ukrainian", "urdu",
             "uyghur", "uzbek", "vietnamese", "welsh", "xhosa", "yiddish", "yoruba", "zulu"]
codes = ["af", "sq", "am", "ar", "hy", "az", 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'zh-CN', 'co', 'hr', 'cs', 'da',
         'nl', 'en', 'eo', 'et', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'he', 'hi', 'hmn',
         'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jv', 'kn', 'kk', 'km', 'rw', 'ko', 'ku', 'ky', 'lo', 'la', 'lv',
         'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'ny', 'or', 'ps', 'fa', 'pl',
         'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv',
         'tl', 'tg', 'ta', 'tt', 'te', 'th', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu']


def audioInput(code, systemLang):
    r = sr.Recognizer()
    while True:
        print("\n" + str(getTranslation("listening...", systemLang)))
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            audio = r.listen(source)
            try:
                userInput = r.recognize_google(audio, language=code)
                print("\n" + userInput)
                return userInput
            except Exception as e:
                print("\n" + str(getTranslation("Sorry, I did not hear that.", systemLang)))
                pass


def getTranslation(text, code):
    toTranslate = TextBlob(text)
    try:
        translatedText = toTranslate.translate(to=code)
    except:
        translatedText = toTranslate

    return translatedText


def getCode(language):
    test = language
    while True:
        for i in range(len(languages)):
            if test.lower() == languages[i]:
                langCode = codes[i]
                return langCode
        speak(str(getTranslation("Did not find " + language + ". Please say a valid language", "en")), "en")
        test = audioInput("en", "en")


count = 0


def speak(text, code):
    global count
    tts = gTTS(text=text, lang=code)
    while True:
        try:
            tts.save(f'audio{count}.mp3')
            break
        except Exception as e:
            pass
    print('\n' + text)
    playsound.playsound(f'audio{count}.mp3')
    count += 1


def startLanguage(systemLang):
    speak(str(getTranslation("What is the language you want to translate from?", systemLang)), systemLang)
    while True:
        language = str(getTranslation(audioInput(systemLang, systemLang), "en")).lower()
        for i in languages:
            if i in language:
                return i
        speak(str(getTranslation("Did not find " + language + ". Please say a valid language", systemLang)), systemLang)


def translateLanguage(systemLang):
    prompt = getTranslation("What is the language you want to translate to?", systemLang)
    speak(str(prompt), systemLang)
    while True:
        language = audioInput(systemLang, systemLang)
        language = str(getTranslation(language, "en")).lower()
        for i in languages:
            if i in language:
                return i
        speak(str(getTranslation("Did not find " + language + ". Please say a valid language", systemLang)), systemLang)


def main():
    speak("What is the language that you speak", "en")
    mainLanguage = audioInput("en", "en")
    mainCode = getCode(mainLanguage)
    inputLanguage = startLanguage(mainCode)
    inputCode = getCode(inputLanguage)
    outputLanguage = translateLanguage(mainCode)
    outputCode = getCode(outputLanguage)
    speak(str(getTranslation("Say what you want to translate", mainCode)), mainCode)
    needTranslation = audioInput(inputCode, mainCode)
    translated = getTranslation(needTranslation, outputCode)
    print("\n'" + needTranslation + "'" + str(getTranslation("  in " + outputLanguage + " is ", mainCode)))
    speak(str(translated), outputCode)


if __name__ == '__main__':
    main()
