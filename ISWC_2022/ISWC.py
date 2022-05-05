from abc import abstractmethod


class ISWC:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def getLemma(word):
        return

    @abstractmethod
    def getTypeOfWord(word):
        return

    @abstractmethod
    def isNumber(word):
        return

    @abstractmethod
    def isVerb(word):
        return

    @abstractmethod
    def isAdjective(word):
        return

    @abstractmethod
    def isAdverb(word):
        return

    '''
    @abstractmethod
    def insertArtworkInDict(instance):
        return
    '''
