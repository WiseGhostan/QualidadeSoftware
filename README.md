# QualidadeSoftware
# 🌄 DF Turismos

Um sistema web desenvolvido com Django para cadastro, gestão e visualização de **pontos turísticos** no Distrito Federal.

## 📚 Funcionalidades

- Cadastro e listagem de turistas
- Cadastro de parques e feiras do DF
- Localização de Pontos turísticos no Google Maps
- Relatórios e gráficos disponíveis para Colaboradores
- Interface estilizada com CSS e FontAwesome

## 🚀 Tecnologias Utilizadas

- Python 3.13.2
- Django 5.2.2
- HTML5 + CSS3
- Django REST Framework (para a criação de APIs)
- Matplotlib
- FontAwesome (ícones)

---

## ⚙️ Como instalar e rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/projeto_df_turismos.git
cd df_turismos
```

### 2. Crie e ative um ambiente virtual

#### Windows:

```bash
python -m venv venv
.env\Scriptsctivate
```

#### Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências do projeto

```bash
pip install -r requirements.txt
```


### 4. Execute as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Rode o servidor

```bash
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---
## ✍️ Autor

Desenvolvido como parte da disciplina **Qualidade Software**  
**Universidade Católica de Brasília – Engenharia de Software (6º semestre)**

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** – use, modifique e distribua livremente.
