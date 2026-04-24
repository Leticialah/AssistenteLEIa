# Funcionamento do sistema

Esta seção descreve o funcionamento interno do Assistente LEIa.

---

## Visão geral

O sistema realiza automação de navegador para acessar páginas web, localizar elementos e monitorar alterações em valores numéricos.

---

## Etapas do processo

### 1. Acesso à página

O sistema utiliza a biblioteca **Playwright** para abrir a página informada pelo usuário.

---

### 2. Localização do elemento

O elemento é identificado através de:

- CSS Selector  
ou  
- XPath  

---

### 3. Extração do valor

Após localizar o elemento:

- O texto é capturado
- Uma expressão regular (Regex) é utilizada para extrair o número

---

### 4. Armazenamento do valor inicial

O primeiro valor identificado é armazenado como referência.

---

### 5. Monitoramento contínuo

O sistema entra em loop, realizando:

- Atualização da página
- Nova leitura do valor
- Comparação com o valor anterior
- Registro das ações e leituras no log

---

### 6. Detecção de alteração

Quando ocorre mudança:

- O evento é registrado no log
- O novo valor substitui o anterior

---

### 7. Envio de alerta

Ao detectar alteração:

- O sistema abre o Gmail
- Cria uma nova mensagem
- Insere automaticamente o valor antigo e o novo valor
- Aciona o botão de envio

---

## Considerações técnicas

- O sistema depende da estrutura da página
- Mudanças no HTML podem afetar o funcionamento
- O envio de e-mail depende da interface do Gmail
