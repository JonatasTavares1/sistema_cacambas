import sys
import os

# Garante que a pasta raiz esteja no path
sys.path.append(os.path.dirname(__file__))

from app.main import main

main()