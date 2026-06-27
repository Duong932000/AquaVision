
from ui.window import MainWindow
from utils.load_config import InitialConfigLoader

def SlothStudio():

    InitialConfigLoader.initialize()
    app = MainWindow(InitialConfigLoader.get_all())
    app.mainloop()

if __name__ == "__main__":

    SlothStudio()
