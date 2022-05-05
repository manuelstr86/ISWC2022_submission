import pycountry
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import treetaggerwrapper
import json
from pprint import pprint
import os
import prototyper_config as cfg

#####################################################
#####################################################
#       VAR GLOBALI                                 #
#####################################################
#####################################################
from ISWC import ISWC

language = cfg.language

remove_words = stopwords.words(  # le stop_words sono prese dalla libreria nltk (sono parole da non considerare)
    pycountry.languages.get(alpha_2=language).name.lower()  # la lingua è derivata dal tag, tramite pycountry
)

remove_words += list(string.punctuation) + ["...", "``"]

if language == "it":
    remove_words += ["di", "a", "da", "in", "su",
                     "il", "del", "al", "dal", "nel", "sul",
                     "lo", "dello", "allo", "dallo", "nello", "sullo",
                     "la", "della", "alla", "dalla", "nella", "sulla",
                     "l’", "dell’", "all’", "dall’", "nell’", "sull’",
                     "i", "dei", "ai", "dai", "nei", "sui",
                     "gli", "degli", "agli", "dagli", "negli", "sugli",
                     "le", "delle", "alle", "dalle", "nelle", "sulle"]
    remove_words += ["il", "lo", "la", "i", "gli", "le", "un", "un'", "uno", "una"]
    remove_words += ["a", "a meno che", "acciocché", "adunque", "affinché", "allora",
                     "allorché", "allorquando", "altrimenti", "anche", "anco", "ancorché",
                     "anzi", "anziché", "appena", "avvegna che", "avvegnaché", "avvegnadioché",
                     "avvengaché", "avvengadioché", "benché", "bensi", "bensì", "che", "ché",
                     "ciononostante", "comunque", "conciossiaché", "conciossiacosaché", "cosicché",
                     "difatti", "donde", "dove", "dunque", "e", "ebbene", "ed", "embè", "eppure",
                     "essendoché", "eziando", "fin", "finché", "frattanto", "giacché", "giafossecosaché",
                     "imperocché", "infatti", "infine", "intanto", "invece", "laonde", "ma", "magari",
                     "malgrado", "mentre", "neanche", "neppure", "no", "nonché", "nonostante", "né", "o",
                     "ogniqualvolta", "onde", "oppure", "ora", "orbene", "ossia", "ove", "ovunque",
                     "ovvero", "perché", "perciò", "pero", "perocché", "pertanto", "però", "poiché",
                     "poscia", "purché", "pure", "qualora", "quando", "quindi", "se", "sebbene",
                     "semmai", "senza", "seppure", "sia", "siccome", "solamente", "soltanto",
                     "sì", "talché", "tuttavia"]

tagger = treetaggerwrapper.TreeTagger(TAGLANG=language)

filename = cfg.jsonDescrFile
filename_output = cfg.lemmatizedDescrFile
dict = {}
# path = "genres_for_cocos_v2/"
encoding = "utf-8"


class Transformer(ISWC):
    def __init__(self, name):
        self.name = "Transformer"

    # metodi per transformer
    def getLemma(word):
        tags = treetaggerwrapper.make_tags(tagger.tag_text(word))
        return tags[0].__getattribute__("lemma").split(":")[0]

    def getTypeOfWord(word):
        tags = treetaggerwrapper.make_tags(tagger.tag_text(word))
        return tags[0].__getattribute__("pos").split(":")[0]

    def isNumber(word):
        return Transformer.getTypeOfWord(word) == "NUM"

    def isVerb(word):
        return Transformer.getTypeOfWord(word) == "VER"

    def isAdjective(word):
        return Transformer.getTypeOfWord(word) == "ADJ"

    def isAdverb(word):
        return Transformer.getTypeOfWord(word) == "ADV"

    def runTransformer(self, logger, fileInputJsonPost):
        global filename
        filename = fileInputJsonPost
        #print("FILE: " + str(filename))
        logger.info('Change directory: Creazione dei prototipi/')
        retval = os.getcwd()
        logger.info('Directory changed successfully ' + str(retval))

        #print("************* " + str(filename))
        file = open(filename, "r", encoding=encoding)

        artworks = json.loads(file.read())
        file.close()

        for artwork in artworks:
            keys = cfg.instanceDescr

            for key in keys:
                only_lemmas = ""
                description = artwork[key]
                word_tokens = word_tokenize(str(description))

                verbo = None
                for word in word_tokens:
                    if "'" in word:  # se la parola e' ad esempio "d'autore", prendo solo "autore"
                        word = word.split("'")[1]

                    word = word.lower()

                    if (len(word) > 1) and (word not in remove_words) and (not Transformer.isNumber(word)) and (
                    not Transformer.isAdverb(word)):

                        if Transformer.isVerb(word):
                            verbo = Transformer.getLemma(word)
                        else:
                            word = Transformer.getLemma(word)

                        if word not in only_lemmas:
                            only_lemmas = only_lemmas + " " + word

                        if verbo is not None:
                            if verbo not in only_lemmas:
                                only_lemmas = only_lemmas + " " + verbo
                            verbo = None

                artwork[key] = only_lemmas

        os.chdir('../Sistema di raccomandazione/Classificatore')
        logger.info('Change directory: Sistema di raccomandazione/Classificatore/')
        retval = os.getcwd()
        logger.info('Directory changed successfully ' + str(retval))
        with open(retval +'/'+ filename_output, "w", encoding=encoding) as outfile:
            json.dump(artworks, outfile, indent=2, ensure_ascii=False)
            logger.info('Write artworks: ' + str(outfile))
            logger.info('Transformer execution terminate successfully!')
