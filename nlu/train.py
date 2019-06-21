import os
import json

from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer, Interpreter
from rasa_nlu import config

dir_path = os.path.dirname(__file__)


class SuperviseTrainer(object):

    def __init__(self,
                 nlu_data=os.path.join(dir_path, 'data/training_data_new.json'),
                 nlu_config=os.path.join(
                     dir_path, 'config/config_jieba_mitie_sklearn.yml'),
                 nlu_model_path=dir_path,
                 ):
        self.nlu_data = nlu_data
        self.nlu_config = nlu_config
        self.nlu_model_path = nlu_model_path

        try:
            interpreter = Interpreter.load(os.path.join(
                dir_path, 'models'))
        except:
            print("Model is not exists. Train it now.")
            self._train_nlu()
            interpreter = Interpreter.load(os.path.join(
                dir_path, 'models'))

    def _train_nlu(self):

        training_data = load_data(self.nlu_data)
        trainer = Trainer(config.load(self.nlu_config))
        trainer.train(training_data)
        # Returns the directory the model is stored in
        trainer.persist(self.nlu_model_path, fixed_model_name="models")

if __name__ == "__main__":
    trainer = SuperviseTrainer()
    