import os
import dotenv
import psycopg2

# Load environment variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file, override=True)


def insert_query(table_name, values):
    print("Creating conncetion:")
    conn = psycopg2.connect(database=os.getenv('POSTGRESQL_DATABASE'),
                            host=os.getenv('POSTGRESQL_HOST'),
                            port=os.getenv('POSTGRESQL_PORT'),
                            user=os.getenv('POSTGRESQL_USER'),
                            password=os.getenv('POSTGRESQL_PASSWORD')
                            )
    conn.autocommit = True
    cursor = conn.cursor()
    print("Execute insert query:")
    query = f'''
    INSERT INTO {table_name} VALUES {values}
    on conflict do nothing
    '''
    cursor.execute(query)
    cursor.close()
    conn.close()
    print("Conncetion closed.")


