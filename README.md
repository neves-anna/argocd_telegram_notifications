# Notificações do ArgoCD no Telegram

## Requisitos
- **Cluster Kubernetes**
- **Python 3.10**
- **Helm**
- **Conta e bot no Telegram**

## Ferramentas Utilizadas
- **Sistema Operacional:** Ubuntu 22.04 (WSL 2)
- **IDE:** Visual Studio Code
- **Cluster Local:** Minikube
- **Criador de Bot Telegram:** BotFather
- **Versão do Python:** 3.10
- **ArgoCD Helm Chart:** 
  - Repositório: `https://argoproj.github.io/argo-helm/`
  - Chart: `argo-cd-7.7.0`
- **HelloWorld Helm Chart:**
  - Repositório: `https://pergon.github.io/Helm3/`
  - Chart: `hello-world:0.3.0`

## Estrutura do Repositório GitHub

Repositório: [argocd_telegram_notifications](https://github.com/neves-anna/argocd_telegram_notifications.git)

### Conteúdo:
```
├── README.md
├── easy_telegram_chat_id                    # Script para obter o chat ID do Telegram
│   ├── argo_chat_id.py                      # Código para capturar IDs de mensagens de privados/grupos/canais
│   └── requirements.txt                     # Dependências do script
└── infra                                    # Arquivos para configurar as notificações ArgoCD
    ├── argo-object.yaml                     # Manifesto do objeto de teste (hello world) no ArgoCD
    ├── argocd-values-notifications.yaml     # Helm Values já editado (somente campos necessários alterados)
    ├── argocd-values.yaml                   # Helm Values da forma que vem no primeiro (get values) após instalação limpa
    └── config-map.yaml                      # ConfigMap das notificações
```


## Considerações

Se você já possui experiência com o ArgoCD e um ambiente com o mesmo em execução, favor pular diretamente para o passo 8. Caso contrário, sugiro que siga o passo a passo desde o começo. Grata desde já, espero que eu possa ajudar.

---

## Configuração do Bot do Telegram e Canais para Notificações

### Passo 1: Criação do Bot no Telegram

1. Envie uma mensagem para o [@BotFather](https://t.me/botfather) com o comando `/newbot`.
2. O BotFather guiará você para definir o nome do seu bot e fornecerá um **Token ID**, que será muito importante para as notificações daqui pra frente.

### Passo 2: Alteração das Configurações de Privacidade do Bot

Para que o bot consiga ler mensagens de grupos e canais, é necessário alterar as configurações de privacidade no BotFather:

1. Envie a mensagem `/mybots` para o BotFather.
2. Selecione o bot que deseja configurar.
3. Clique em "Group Privacy" e desative essa opção.

---

## Passo 3: Utilização do Script para Obter o Chat ID no Telegram

O script irá retornar o chat ID de conversas privadas, grupos ou canais. Guia de uso e mais informações sobre o funcionamento desse script, [aqui](https://github.com/neves-anna/argocd_telegram_notifications/blob/main/easy_telegram_chat_id/README.md).

---

### Passo 4: Instalação do Minikube 
Execute os seguintes comandos em ordem:
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb

sudo dpkg -i minikube_latest_amd64.deb

sudo usermod -aG docker $USER

minikube start
```
### Passo 5: Instalando o Helm e Adicionando o Repositório do ArgoCD ao Seu Ambiente
1. Siga as instruções de instalação do [Helm](https://helm.sh/docs/intro/install/) para seu ambiente.

2. Execute o seguinte comando para adicionar o repositório oficial do ArgoCD:

```bash
helm repo add argo https://argoproj.github.io/argo-helm/
```

### Passo 6: Atualizando o Repositório do Helm

Execute o comando abaixo para atualizar os repositórios de charts no seu ambiente:

```bash
helm repo update
```

### Passo 7: Instalando o Chart do ArgoCD

Instale o Chart do ArgoCD com o seguinte comando:

```bash
helm install argocd argo/argo-cd --namespace argocd --create-namespace
```

## Passo 8: Editando o Arquivo de Valores do Chart do ArgoCD 

Após a instalação, você pode exportar os valores padrão do Chart do ArgoCD para um arquivo local e editá-los conforme necessário:

```bash
helm show values argo/argo-cd > argocd-values.yaml
```

## Arquivos de Referência

No arquivo `argocd-values.yaml`, edite os seguintes campos:

- **Chave de configuração:** `notifications`
- **Subchaves:** `argocdUrl`, `notifiers`, `secret`, `templates`, `triggers`

Referências adicionais para as edições:

- Arquivo de referência com as edições: `infra/argocd-values-notifications.yaml`
- Arquivo `argocd-values.yaml` completo e já editado: `infra/argocd-values.yaml`
- `ConfigMap` para edição do conteúdo das mensagens enviadas para o Telegram: `infra/config-map.yaml`

## Passo 9: Aplicação do Novo Arquivo de Valores do ArgoCD

Após editar o arquivo de valores, aplique-o ao ArgoCD com o comando:

```bash
helm upgrade argocd argocd/argo-cd -f argocd-values.yaml --namespace argo-cd
```

> **Nota:** Convém forçar o reinício do pod `argocd-notifications-controller` para garantir que as novas configurações sejam carregadas corretamente.

## Passo 10: Acesso à GUI do ArgoCD para Adição de Annotations no Aplicativo

Para acessar a interface do ArgoCD via `localhost`, faça um `port-forward` com o comando:

```bash
kubectl port-forward service/argocd-server -n argocd 8080:443
```

Para recuperar a senha de primeiro acesso do ArgoCD, use:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```


## Teste de Notificações

Para fins de teste, foi criada a aplicação `helloworld` via YAML, disponível em `infra/argo-object`. Após a criação da aplicação, basta editar via GUI as configurações da aplicação, no campo **Notification Subscriptions**;

O `chat-id` ao qual me refiro é o da conversa no Telegram, obtido pelo script Python no passo 3.

O campo **Notification Subscriptions** segue o seguinte formato:

```plaintext
notifications.argoproj.io/subscribe.<trigger>.<service>=<chat-id>
```

- **`<trigger>`**: Nome do evento que dispara a notificação. (configurado no values, facilmente consultável no configMap)
- **`<service>`**: Serviço de notificação, neste caso o Telegram.
- **`<chat-id>`**: ID da conversa no Telegram; caso seja mais de um, separe-os por ponto e vírgula (`;`).

**Exemplo de uso:**

```plaintext
notifications.argoproj.io/subscribe.on-deployed.telegram=11111111;-111111111
```

Neste exemplo:
- O `trigger` é `on-deployed`, ativando a notificação após o deploy.
- O `service` é `telegram`.
- O `chat-id` inclui dois IDs separados por ponto e vírgula: `11111111` e `-111111111`.
