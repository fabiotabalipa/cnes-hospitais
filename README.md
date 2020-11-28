# cnes-hospitais

![logo](https://user-images.githubusercontent.com/37602229/100513123-dc1c0a00-314d-11eb-95f8-3f960e3fce60.png)

Rotina em python para obtenção de dados relevantes dos hospitais brasileiros via **Cadastro Nacional de Estabelecimentos de Saúde (CNES)**.

O script realiza um ETL para:

* **E**xtract: base de dados mais recente do CNES via FTP
* **T**ransform: cruzamentos, limpeza e organização dos dados relevantes
* **L**oad: geração do arquivo `cnes-hospitais.csv` no diretório raiz do script, pronto para análise

---

#### Instruções

```shell
pip install -r requirements.txt
python cnes-hospitais.py
```

> python 3.8.6

---

![example](https://user-images.githubusercontent.com/37602229/100513066-d8888300-314d-11eb-9a4c-09622d6cfd86.png)

---
Autor: Fábio Tabalipa

Licença: MIT

> Fiquem à vontade para contribuir via *pull request* 🧑🏽‍💻