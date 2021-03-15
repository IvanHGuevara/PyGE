from pathlib import Path

class GrammarWrapper:
    def __init__(self, grammarFile) -> None:
        grammarText = Path(grammarFile).read_text()
        self.grammar = grammarText
    
    def getProductionRules(self):
        return self.grammar.split("\n")
    
    def getDivisor(self):
        return len(self.getProductionRules())
    
    def getNumberOfProductionRules(self):
        return len(self.getProductionRules())

    def getProductionRuleNumber(self, number):
        return self.getProductionRules()[number]

    def getNumberDefinitions(self):
        return len(list(map(lambda x: x[1].split("|"),list(map(lambda x: x.split(":="), self.grammar.getProductionRules())))))
