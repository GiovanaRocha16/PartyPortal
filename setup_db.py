from app.models.database import Database

db = Database()
db.initialize_database()

print("Banco criado / atualizado com sucesso.")