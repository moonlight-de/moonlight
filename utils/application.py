from widgets import init
from ignis.app import IgnisApp

# Initialize the app first
app = IgnisApp()

app_instance = IgnisApp.get_initialized()
app_instance.run(init())
