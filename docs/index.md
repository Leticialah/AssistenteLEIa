# Assistente LEIa

O **Assistente LEIa** é uma aplicação desenvolvida em Python para monitorar valores numéricos em páginas web e enviar alertas automáticos por e-mail sempre que uma alteração for identificada.

---

## Objetivo do sistema

O objetivo principal do sistema é automatizar o acompanhamento de valores em páginas web, evitando que o usuário precise verificar manualmente se determinada informação foi alterada.

A aplicação localiza um valor na página por meio de um seletor **CSS** ou **XPath**, extrai o número encontrado e passa a monitorá-lo em intervalos definidos pelo usuário.

---

## Principais funcionalidades

- Monitoramento contínuo de valores em páginas web
- Localização de elementos utilizando CSS Selector ou XPath
- Extração de valores numéricos por expressão regular
- Registro das ações e alterações identificadas
- Envio automático de alerta por e-mail
- Interface gráfica simples e intuitiva

---

## Fluxo geral de funcionamento

1. O usuário informa seu nome, a URL da página e o seletor do valor desejado.
2. O sistema acessa a página utilizando automação de navegador.
3. O valor numérico é localizado e extraído.
4. O sistema passa a verificar periodicamente se houve alteração.
5. Ao detectar mudança, a alteração é registrada no log.
6. Um e-mail de alerta é enviado para o destinatário informado.

---

## Tecnologias utilizadas

- **Python**
- **Tkinter**
- **Playwright**
- **Regex**
- **Gmail**
- **MkDocs**

---

## Resumo

O Assistente LEIa funciona como um assistente automatizado de monitoramento web, permitindo acompanhar alterações em valores de páginas online de forma prática, visual e com notificação por e-mail.