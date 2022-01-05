import os

DB_PROVIDER = os.environ.get('DATABASE_PROVIDER', 'sqlite')  # valid choices : sqlite, mysql, postgres
DB_URL = os.environ.get('DATABASE_URL', os.path.join(os.getcwd(), 'bot.db'))  # file path in case of sqlite
