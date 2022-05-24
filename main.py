import os
import sys

from PyQt6.QtWidgets import QApplication
from settings import Settings
from operation import Operation
from results import Results

def main():
    check_file_settings = os.path.exists('settings.yaml')
    settings = Settings()
    result = Results()
    app = QApplication(sys.argv)
    if check_file_settings is True:
        settings.read_settings('settings.yaml')
    else:
        settings.create_settings('settings.yaml')
    core = Operation(settings, result)
    core.window_show()

    app.exec()

if __name__ == '__main__':
    main()
