import subprocess
import sys
import psycopg2

def start_scrapy_for_url(url, stop, site_id):
    # Comando para iniciar o Scrapy para uma URL específica
    command = [sys.executable, '-m', 'scrapy', 'runspider', 'coletor.py', '-a', f'file={url}', '-a', f'stop={stop}', '-a', f'site_id={site_id}']
    subprocess.run(command, check=True)

def main():
    if len(sys.argv) < 2:
        print("Uso: main.py <stop>")
        sys.exit(1)

    stop = sys.argv[1]

    # Verificar se o argumento 'stop' é um número inteiro
    try:
        stop = int(stop)
    except ValueError:
        print("O argumento 'stop' deve ser um número inteiro.")
        sys.exit(1)

    # Conectar ao banco de dados PostgreSQL
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="crazydata",
            host="localhost",
            port="5435",
            database="framecolector"
        )

        cursor = connection.cursor()

        # Consultar as URLs e seus respectivos site_id do banco de dados
        cursor.execute("SELECT url, site_id FROM opendata.sites")
        rows = cursor.fetchall()

        # Iniciar o processo do Scrapy para cada URL
        for row in rows:
            url = row[0]
            site_id = row[1]
            start_scrapy_for_url(url, stop, site_id)
             # Atualizar o status para 1 após a coleta
            try:
                cursor.execute("UPDATE opendata.sites SET status = 1 WHERE site_id = %s", (site_id,))
                connection.commit()
            except (psycopg2.Error, psycopg2.DatabaseError) as error:
                print(f"Erro ao atualizar o status do site_id {site_id}: {error}")


    except (psycopg2.Error, psycopg2.DatabaseError) as error:
        print("Erro ao conectar ou consultar o banco de dados PostgreSQL:", error)
        sys.exit(1)
    finally:
        # Fechar a conexão com o banco de dados
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    main()
