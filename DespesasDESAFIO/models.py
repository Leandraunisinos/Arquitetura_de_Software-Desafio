import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class Despesa:
    """Model que representa uma despesa e contém as regras de negócio"""
    
    def __init__(self, id: int = None, descricao: str = None, valor: float = None, data: str = None):
        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.data = data
    
    @staticmethod
    def get_db_connection():
        """Estabelece conexão com o banco de dados SQLite"""
        conn = sqlite3.connect('despesas.db')
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def init_db():
        """Inicializa o banco de dados criando a tabela se não existir"""
        conn = Despesa.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    @staticmethod
    def validar_despesa(descricao: str, valor: float, data: str) -> tuple:
        """
        REGRA DE NEGÓCIO a: Toda despesa deve possuir uma descrição e um valor
        REGRA DE NEGÓCIO b: Uma despesa deve possuir uma data
        Retorna (is_valid, mensagem_erro)
        """
        if not descricao or descricao.strip() == "":
            return False, "A descrição é obrigatória"
        
        if valor is None or valor <= 0:
            return False, "O valor deve ser maior que zero"
        
        if not data:
            return False, "A data é obrigatória"
        
        # Valida formato da data
        try:
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            return False, "Data inválida. Use o formato AAAA-MM-DD"
        
        return True, ""
    
    def salvar(self) -> bool:
        """
        REGRA DE NEGÓCIO c: O usuário pode cadastrar despesas
        Salva uma nova despesa no banco de dados
        """
        # Validação antes de salvar
        valido, erro = Despesa.validar_despesa(self.descricao, self.valor, self.data)
        if not valido:
            return False
        
        conn = Despesa.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO despesas (descricao, valor, data)
            VALUES (?, ?, ?)
        ''', (self.descricao, self.valor, self.data))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()
        return True
    
    @staticmethod
    def remover(despesa_id: int) -> bool:
        """
        REGRA DE NEGÓCIO d: O usuário pode remover despesas
        Remove uma despesa do banco de dados pelo ID
        """
        conn = Despesa.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM despesas WHERE id = ?', (despesa_id,))
        conn.commit()
        removido = cursor.rowcount > 0
        conn.close()
        return removido
    
    @staticmethod
    def listar_todas() -> List[Dict]:
        """Retorna todas as despesas cadastradas"""
        conn = Despesa.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM despesas ORDER BY data DESC, id DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def calcular_total(despesas: List[Dict] = None) -> float:
        """
        REGRA DE NEGÓCIO e: O sistema deve calcular o total de despesas
        Se despesas for passado, calcula sobre a lista. Caso contrário, busca no banco
        """
        if despesas is None:
            despesas = Despesa.listar_todas()
        
        total = sum(despesa['valor'] for despesa in despesas)
        return round(total, 2)
    
    @staticmethod
    def calcular_total_por_periodo(data_inicio: str, data_fim: str) -> float:
        """Calcula o total de despesas em um período específico"""
        conn = Despesa.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(valor) as total FROM despesas 
            WHERE data BETWEEN ? AND ?
        ''', (data_inicio, data_fim))
        row = cursor.fetchone()
        conn.close()
        total = row['total'] if row['total'] is not None else 0
        return round(total, 2)