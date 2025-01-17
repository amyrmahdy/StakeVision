import os
import dotenv
import psycopg2

# Load environment variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file, override=True)

def read_query(table_name):
    print("Creating conncetion:")
    conn = psycopg2.connect(database=os.getenv('POSTGRESQL_DATABASE'),
                            host=os.getenv('POSTGRESQL_HOST'),
                            port=os.getenv('POSTGRESQL_PORT'),
                            user=os.getenv('POSTGRESQL_USER'),
                            password=os.getenv('POSTGRESQL_PASSWORD')
                            )
    conn.autocommit = True
    cursor = conn.cursor()
    print("Execute select query:")
    query = f'''
    SELECT * FROM {table_name} ;
    '''
    cursor.execute(query)
    retrieved_rows = cursor.fetchall()
    cursor.close()
    conn.close()
    print("Conncetion closed.")
    return retrieved_rows


