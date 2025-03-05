# Diário de Aprendizado

Este projeto é uma aplicação web que permite que seus usuários criem, editem, vejam e excluem **entradas** sobre **tópicos** adicionados pela administração.

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/pdr-guilherme/diario-de-aprendizado.git
    cd diario-de-aprendizado
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv .venv
    source venv/bin/activate  # Para Linux/macOS
    venv\Scripts\activate     # Para windows
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados:

    ```bash
    python manage.py migrate
    ```

5. Crie um superusuário para acessar o admin:

    ```bash
    python manage.py createsuperuser
    ```

6. Inicie o servidor
    ```bash
    python manage.py runserver
    ```

## Testes

Testes para o projeto estão disponíveis dentro da pasta `diario/testes`, para executá-los, rode o seguinte comando dentro da pasta:

```bash
python manage.py test
```

## Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE.txt) para mais detalhes.
