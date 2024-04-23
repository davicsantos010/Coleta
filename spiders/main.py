import subprocess
import sys
import csv

def start_scrapy_for_url(url, stop):
    # Comando para iniciar o Scrapy para uma URL específica
    command = [sys.executable, '-m', 'scrapy', 'runspider', 'coletor.py', '-a', f'file={url}', '-a', f'stop={stop}']
    subprocess.run(command, check=True)

def main():
    if len(sys.argv) < 3:
        print("Uso: python start_scrapy_for_urls.py <arquivo_urls> <stop>")
        sys.exit(1)

    arquivo_urls = sys.argv[1]
    stop = sys.argv[2]

    # Verificar se o argumento 'stop' é um número inteiro
    try:
        stop = int(stop)
    except ValueError:
        print("O argumento 'stop' deve ser um número inteiro.")
        sys.exit(1)

    # Ler as URLs do arquivo CSV
    urls = []
    with open(arquivo_urls, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Verifica se a linha não está vazia
                url = row[0].strip()  # Obtém a URL e remove espaços em branco
                urls.append(url)

    # Iniciar o processo do Scrapy para cada URL
    for url in urls:
        start_scrapy_for_url(url, stop)

if __name__ == '__main__':
    main()
