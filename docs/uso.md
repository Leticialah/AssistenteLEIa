# Como utilizar o Assistente LEIa

Esta seção descreve o passo a passo para utilizar corretamente o sistema.

---

## Etapa 1 — Login no Gmail

Antes de iniciar o monitoramento, é necessário realizar o login no Gmail:

- Clique no botão **"Abrir Gmail"**
- Realize o login manual no navegador aberto
- Essa etapa é necessária para permitir o envio automático de e-mails

---

## Etapa 2 — Configuração do monitoramento

Preencha os campos da interface:

- **Nome do usuário**  
  Deve conter ao menos 3 caracteres

- **URL da página**  
  Endereço da página que contém o valor a ser monitorado

- **Tipo de seletor**  
  - CSS Selector  
  - XPath  

- **Seletor do elemento**  
  Caminho até o elemento que contém o valor desejado

- **E-mail de destino**  
  Endereço que receberá o alerta

- **Intervalo de verificação**  
  Tempo entre cada leitura (em segundos)

- **Timeout**  
  Tempo máximo de espera para localizar o elemento

---

## Etapa 3 — Validação do valor

Antes de iniciar:

- Verifique se o sistema está capturando corretamente o valor
- Observe os logs exibidos na interface

---

## Etapa 4 — Iniciar monitoramento

Clique em **"Iniciar Monitoramento"**

O sistema irá:

- Capturar o valor inicial
- Iniciar o monitoramento contínuo
- Registrar todas as alterações detectadas

---

## Dicas de uso

- Utilize seletores específicos para evitar erros
- Teste o seletor no navegador antes de usar
- Evite páginas com carregamento muito dinâmico sem ajuste de timeout