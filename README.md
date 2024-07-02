<h1 align="center">LOVE PETS</h1>
 
O projeto irá adotar as seguintes tecnologias:

- **[Python](https://www.python.org/)**: linguagem;
- **[Django](https://www.djangoproject.com/)**: aplicação cliente na web;
- **[MySql](https://www.mysql.com/)**: base de dados;



<h1 align="center">INSTALACAO</h1>

git clone (key_project)

python3 -m venv nome_do_ambiente_virual

pip install -r requirements.txt

python3 manage.py migrate

python3 manage.py runserver





dessa forma não esta funcionando e não vai funcionar, estou pensando em criar uma tabela na base de dados com o intervalo de uma em uma hora referente ao dia, e a cada serviço que  é agendado esse campo na base ficar preenchido, assim se tiver um serviço com duração maior que 2 horas o sistema preenche dois campo. Dessa forma fica viavel ? 