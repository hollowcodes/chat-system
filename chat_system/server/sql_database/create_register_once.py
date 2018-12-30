from chat_system.server.sql_database import sql_handler

# creates new sql database called registry (resets the entire database if it is already set up)


def create_register():
    d = sql_handler.database()
    d.create_register_table()

