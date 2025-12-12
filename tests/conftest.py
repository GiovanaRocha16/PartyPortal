import sys
import os

# Caminho da pasta raiz do projeto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Adiciona ao PYTHONPATH
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
