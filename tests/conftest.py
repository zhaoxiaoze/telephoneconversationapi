import os
import sys
import shutil
import pytest

from rasa_nlu.model import Interpreter

here = os.path.abspath(os.path.dirname(__file__))
source_root = os.path.abspath(os.path.join(here, '..'))

if source_root not in sys.path:
    sys.path.append(source_root)

from interface import DialogueManager
from core.status import Message


@pytest.fixture(scope="session")
def nlu_interpreter():
    manager = DialogueManager()
    interpreter = manager.interpreter
    return interpreter

@pytest.fixture(scope="session")
def message():
    return Message

@pytest.fixture(scope="session")
def dialogue_manager():
    log_dir = os.path.join(source_root, 'log/test/')
    shutil.rmtree(log_dir)
    manager = DialogueManager(log_dir=log_dir)
    return manager
