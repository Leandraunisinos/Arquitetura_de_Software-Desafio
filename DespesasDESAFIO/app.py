from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import Despesa

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessao'

# Inicializa o banco de dados
Despesa.init_db()

@app.route('/')
def index():
    """Página principal - lista todas as despesas"""
    despesas = Despesa.listar_todas()
    total = Despesa.calcular_total(despesas)
    return render_template('index.html', despesas=despesas, total=total)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    """
    REGRA DE NEGÓCIO c - Controller orquestra o cadastro
    Recebe dados do formulário e chama o Model para salvar
    """
    descricao = request.form.get('descricao', '').strip()
    try:
        valor = float(request.form.get('valor', 0))
    except ValueError:
        valor = 0
    data = request.form.get('data', '')
    
    # Cria objeto Despesa
    nova_despesa = Despesa(descricao=descricao, valor=valor, data=data)
    
    # Tenta salvar (a validação acontece dentro do Model)
    if nova_despesa.salvar():
        flash('Despesa cadastrada com sucesso!', 'success')
    else:
        flash('Erro ao cadastrar despesa. Verifique os dados.', 'error')
    
    return redirect(url_for('index'))

@app.route('/remover/<int:despesa_id>', methods=['POST'])
def remover(despesa_id):
    """
    REGRA DE NEGÓCIO d - Controller orquestra a remoção
    Chama o Model para remover a despesa pelo ID
    """
    if Despesa.remover(despesa_id):
        flash('Despesa removida com sucesso!', 'success')
    else:
        flash('Erro ao remover despesa.', 'error')
    
    return redirect(url_for('index'))

@app.route('/relatorio')
def relatorio():
    """Exibe relatório com total por período"""
    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')
    
    despesas = Despesa.listar_todas()
    total_geral = Despesa.calcular_total(despesas)
    total_periodo = None
    
    if data_inicio and data_fim:
        total_periodo = Despesa.calcular_total_por_periodo(data_inicio, data_fim)
        # Filtra despesas do período para exibição
        despesas_periodo = [d for d in despesas if data_inicio <= d['data'] <= data_fim]
    else:
        despesas_periodo = despesas
    
    return render_template('relatorio.html', 
                         total_geral=total_geral,
                         total_periodo=total_periodo,
                         despesas=despesas,
                         despesas_periodo=despesas_periodo if 'despesas_periodo' in locals() else despesas,
                         data_inicio=data_inicio,
                         data_fim=data_fim)

@app.route('/api/total')
def api_total():
    """API para obter o total (exemplo de endpoint)"""
    total = Despesa.calcular_total()
    return jsonify({'total': total})

if __name__ == '__main__':
    app.run(debug=True, port=5000)