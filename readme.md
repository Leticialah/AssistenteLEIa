# 📊 Assistente LEIa

Sistema de monitoramento automático de valores em páginas web com envio de alerta por e-mail.

---

## 📌 Descrição

O **Assistente LEIa** é uma aplicação desenvolvida em Python que permite monitorar valores numéricos em páginas web utilizando seletores **CSS ou XPath**.

Quando o valor monitorado sofre alteração, o sistema:
- Detecta automaticamente a mudança
- Registra a alteração no log
- Envia um alerta por e-mail utilizando o Gmail

---

## ⚙️ Funcionalidades

- Monitoramento contínuo de valores em páginas web  
- Suporte a seletores CSS e XPath  
- Extração automática de números do conteúdo da página  
- Detecção de alterações em tempo real  
- Envio automático de e-mails de alerta  
- Interface gráfica com Tkinter  
- Registro de logs de execução  

---

## 🧑‍💻 Como utilizar

### 1. Fazer login no Gmail
Clique no botão **"Abrir Gmail"** e realize o login manual.

### 2. Inserir os dados
Preencha os campos:
- Nome do usuário
- URL da página
- Tipo de seletor (CSS ou XPath)
- Seletor do elemento
- E-mail de destino
- Intervalo de verificação
- Timeout

### 3. Verificar o valor
Certifique-se de que o sistema consegue capturar corretamente o valor da página.

### 4. Iniciar monitoramento
Clique em **"Iniciar Monitoramento"**.

---

## 📈 Funcionamento do sistema

1. A página é aberta utilizando Playwright  
2. O sistema localiza o elemento com base no seletor informado  
3. O valor numérico é extraído do texto  
4. O valor inicial é armazenado  
5. O sistema verifica periodicamente o valor  
6. Ao detectar mudança:
   - Registra no log  
   - Envia e-mail automaticamente  

---

## 🧠 Complexidade (Big O)

O sistema possui complexidade aproximada:

- **O(n)** por verificação, onde *n* é o tamanho do texto do elemento analisado

A cada ciclo:
- leitura do elemento → O(1)  
- extração do número (regex) → O(n)  

Como o processo é repetido em intervalos, o custo total depende do tempo de execução.

---

## 🧾 Logs do sistema

O sistema registra:

- Ações do usuário (início do monitoramento)
- Parâmetros utilizados (URL, seletor, e-mail)
- Valor inicial detectado
- Alterações identificadas
- Erros de execução

---

## 🧪 Testes

Atualmente, o sistema pode ser testado manualmente através da interface.

Sugestões de testes automatizados:
- Validação de nome do usuário  
- Extração de número via regex  
- Validação de configurações  

---

## 🛠️ Tecnologias utilizadas

- Python  
- Tkinter  
- Playwright  
- Regex  
- Automação de navegador  

---

## ⚠️ Observações importantes

- O envio de e-mails depende da interface do Gmail e pode sofrer alterações  
- O sistema pode gerar muitos alertas em valores altamente dinâmicos (ex: criptomoedas) 

---

## 👥 Autor(es)

- Leticia Lavigne Guedes Germano - 2322082002
- Kauã da Silva Araújo - 2322082009
- Cauê Lovis Santana - 2412082008
