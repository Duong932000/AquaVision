
from utils.load_config import InitialConfigLoader
from ui.window import MainWindow

def SlothStudio():

    InitialConfigLoader.initialize()
    app = MainWindow(InitialConfigLoader.get_all())
    app.mainloop()

if __name__ == "__main__":

    SlothStudio()
