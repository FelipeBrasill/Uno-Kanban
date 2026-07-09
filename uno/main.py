import webview
from backend.api.partida_api import PartidaAPI

if __name__ == "__main__":
    api = PartidaAPI()
    webview.create_window(
        "KUBUNO",
        url="http://localhost:5173",  # aponta pro seu Vite rodando em dev
        js_api=api,
    )
    webview.start(gui='qt')