from rasa_nlu.model import Interpreter

interpreter = Interpreter.load('models/default/model_20190514-121130')
test=interpreter.parse(u"没去看病")
print(test)