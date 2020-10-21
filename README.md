# Clockify Star :star:
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fheitordeep%2Fclockify&count_bg=%23548CC7&title_bg=%23555555&icon=gumtree.svg&icon_color=%238CC267&title=Visitas&edge_flat=false)](https://hits.seeyoufarm.com)
<img src='https://img.shields.io/badge/License-MIT-informational'>

## :computer: Sobre o projeto:
Clockify Star: O objetivo é ajudar pessoas a registrar seu ponto sem precisar acessar o site clockify. <br>
O projeto está em desenvolvimento, mas você já pode contar com as seguintes funções:
- [x] Bater ponto no sistema Clockify - Start
- [x] Deslogar no sistema - Stop
- [x] Consultar ID's (Tags, Projetos, Task)
- [ ] Consultar horas trabalhadas :wrench:
- [ ] Bater ponto de entrada e sáida - Start + Stop :wrench:
- [X] Automatizar processos de execução no Airflow

## :pushpin: Pré-requisitos:

- Biblioteca para o projeto: ![PyPI](https://img.shields.io/pypi/v/requests?label=Requests&style=plastic)
- Linguagem: ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requests?label=Python&logo=PYTHON&logoColor=yellow&style=plastic)
- Virtualenv: A preferência é sua :smile:, mas foi utilizado o pyenv.
- Docker: <img src="https://img.shields.io/badge/Airflow-v1.10.9-informational">

## :pushpin: Modo de instalação:
- Requirements: Contém todas as bibliotecas necessárias para rodar o script.
- MakeFile: ```$ make requirements```


## :closed_lock_with_key: Credencial:

- É necessário criar um arquivo ```.env``` com as credenciais:

    - **key**=chave-key_api<br>
    - **workspaces**=id_empresa<br>
    - **user**=id_usuário<br>


## :alarm_clock: Airflow:
- Automatizar execuções no **Airflow**:
    - Primeiro precisamos criar o nosso container:<br>
      ```shell
       $ make up
      ```

    - Em seguida, vamos mover os arquivos do projeto para dentro do container. Foi criado uma pasta no seu host, o caminho seria **/opt/airflow**:

        ```shell
       $ sudo cp -r clockify_star/ /opt/airflow/dags/
        ```

    - Precisamos dar permissão de escrita nos arquivos que encontra- se no diretório **job**:
      ```shell
       $ chmod 777 /opt/airflow/dags/clockify_star/job/*
      ```

- Agora, precisamos instalar as bibliotecas no docker:
   - Criando env e instalando bibliotecas:

      ```shell
      $ make access
      ```
      ```shell
      airflow@7669e2e827fa:~$ python -m venv venv
      ```

      ```shell
      airflow@7669e2e827fa:~$ . venv/bin/activate
      ```

      ```shell
      airflow@7669e2e827fa:~$  pip -r install dags/clockify_star/requirements/requirements_dev.txt
      ```

      ```shell
      airflow@7669e2e827fa:~$ airflow scheduler
      ````
      <br><br>

- Acessar o Airflow:
    http://0.0.0.0:8080/admin/

    ![airflow](https://user-images.githubusercontent.com/17969551/94273742-2f3dca80-ff1b-11ea-8204-9ae0dafb3039.png)

- OBS: As definições de horas e configuração das task é definida no arquivo **scheduler_clockify.py**
- OBS 2: Quando for necessário mudar as tags no clockify, será necessário mover o arquivo **start_job.json** atualizado para **/opt/airflow/dags/clockify_star/job/** dentro do container.


- É necessário também criar um arquivo ```start_job.json``` na pasta **job**:

    Caso não tenha **taskId** no projeto atual, coloque dessa forma o json:

    ```javascript
    {
        "projectId": "id_projeto",
        "billable": "true ou false",
        "description": "Descrição",
        "tagIds": ["Python", "Linux", "Google Cloud Storage", "Git"],
        "taskId": 0

    }
    ```

    Caso tenha **taskId**:

    ```javascript
    {
        "projectId": "id_projeto",
        "billable": "true ou false",
        "description": "Descrição",
        "tagIds": ["Python", "Linux", "Google Cloud Storage", "Git"],
        "taskId": "5e83a6blabla"

    }
    ```

## :warning:  Obtendo os ID's:

- ID Projeto: ```$ make get_param id=get_project```
- ID Tags: ```$ make get_param id=get_tags```
- Lista ID's do Projeto: ```$ make get_param id=list_projects```
- ID Task: ```$ make get_param id="get_task id_project"```

- Resultado do diretório: <br>
![Captura de tela de 2020-08-24 14-59-01](https://user-images.githubusercontent.com/17969551/91079454-708c4300-e61a-11ea-86db-a9d48e3ea25d.png)


## 🚀 Executar script fora do Docker:
- No modo executar, possui dois paramêtros, **start** e **stop**

- Caso esteja utilizando **pyenv**:
  - Iniciar o dia de trabalho: ```$ sh run.sh start```  
  - Encerrar o dia de trabalho: ```$ sh run.sh stop```  
- Caso esteja utilizando outra virtualização:
  - Iniciar o dia de trabalho: ```$ make run job=start```
  - Encerrar o dia de trabalho: ```$ make run job=stop```
