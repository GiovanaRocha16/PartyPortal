from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')


@app.route('/')
def action_home(info=None):
    return ctl.render('home')


@app.route('/confeiteiro', method=['GET', 'POST'])
def confeiteiro():
    if request.method == 'POST':
        ing1 = request.forms.get('ing1')
        ing2 = request.forms.get('ing2')
        ing3 = request.forms.get('ing3')

        receitas = {
            ('Chocolate', 'Morango', 'Leite'): "Um bolo de morango delicioso! 🍰",
            ('Limão', 'Leite', 'Morango'): "Um mousse cítrico refrescante! 🍋🍓",
            ('Pimenta', 'Alho', 'Limão'): "🤢 Uma torta explosiva de alho e pimenta!",
            ('Chocolate', 'Leite', 'Pimenta'): "🔥 Um chocolate picante ousado!",
        }

        chave = (ing1, ing2, ing3)
        resultado = receitas.get(chave, f"🍽️ Uma criação misteriosa de {ing1}, {ing2} e {ing3}!")
        return template('app/views/html/confeiteiro', resultado=resultado)
    else:
        return template('app/views/html/confeiteiro', resultado=None)
    
    
@app.route('/campo_minado', method=['GET', 'POST'])
def campo_minado():
    import random

    bomba = random.randint(1, 9)
    resultado = None
    clicados = []

    if request.method == 'POST':
        escolha = int(request.forms.get('escolha'))
        clicados = request.forms.get('clicados', '')
        clicados = [int(c) for c in clicados.split(',') if c]

        if escolha not in clicados:
            clicados.append(escolha)

        if escolha == bomba:
            resultado = f"💥 BOOM! Você pisou na bomba!"
        elif len(clicados) == 8:
            resultado = "🏆 Parabéns! Você venceu sem explodir!"
        else:
            resultado = f"✅ {len(clicados)} tentativas seguras!"

    return template(
        'app/views/html/campo_minado',
        resultado=resultado,
        clicados=clicados,
        bomba=bomba
    )

if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
