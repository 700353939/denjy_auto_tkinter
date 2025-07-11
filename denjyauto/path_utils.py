import sys
import os

def resource_path(relative_path):
    """Връща абсолютен път до ресурса, работи и с PyInstaller .exe"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)