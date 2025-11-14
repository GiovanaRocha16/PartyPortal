from bottle import template


class Application():

    def __init__(self):
        self.pages = {
            'pagina': self.pagina,
            'home': self.home
        }

    def render(self, page):
        print(f"[DEBUG] Render solicitado para: {page}")
        content = self.pages.get(page, self.helper)
        return content()

    def helper(self):
        try:
            return template('app/views/html/helper')
        except:
            return "<h3>Template 'helper.tpl' não encontrado.</h3>"

    def home(self):
        print("[DEBUG] Entrou em home()")
        return template('app/views/html/home')

    def pagina(self):
        return template('app/views/html/pagina')
