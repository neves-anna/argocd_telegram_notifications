
Uma das maiores dificuldades ao lidar com posts no Telegram é obter os IDs de conversas privadas, grupos ou canais. Para simplificar esse processo, criei um script que facilita o resgate desses valores de forma simples e prática, tornando mais fácil utilizar esses dados no envio de notificações no ArgoCD.

### Passo a Passo para Configuração do Script de Notificações no Telegram

1. **Instalar Python 3.10** (caso ainda não esteja instalado):
   ```bash
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt install python3.10 python3.10-venv python3.10-dev
   ```

2. **Criar um ambiente virtual** com `venv`:
   ```bash
   python3.10 -m venv argo
   ```

3. **Ativar o ambiente virtual**:
   ```bash
   source argo/bin/activate
   ```

4. **Instalar os requisitos** listados no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

5. **Adicionar o token** recebido do BotFather no arquivo `.py`.

6. **Executar o script**:
   ```bash
   python3.10 ./argo_chat_id.py
   ```

> **Observação:** Os logs serão gerados apenas quando você enviar uma mensagem direta para o bot ou adicioná-lo em um grupo ou canal.  
> Para habilitar a leitura de mensagens de grupos e canais, é necessário ajustar as configurações de privacidade do bot no BotFather:
   - Envie a mensagem `/mybots` para o BotFather.
   - Selecione o bot que deseja configurar.
   - Clique em "Group Privacy" e desative essa opção. 

Isso permitirá que o bot leia mensagens em grupos e canais, conforme necessário para as notificações.
