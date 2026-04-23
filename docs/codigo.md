# Estrutura do código

Esta seção apresenta a organização e principais componentes do sistema.

---

## Organização geral

O sistema é estruturado em funções responsáveis por:

- Interface gráfica
- Validação de dados
- Automação do navegador
- Monitoramento
- Envio de e-mail

---

## Principais funções

### start_monitoring()

Responsável por:

- Validar os dados inseridos
- Iniciar o processo de monitoramento
- Registrar logs iniciais

---

### read_value()

Responsável por:

- Localizar o elemento na página
- Capturar o texto
- Extrair o valor numérico

---

### extract_number()

Responsável por:

- Processar o texto capturado
- Utilizar Regex para extrair números
- Retornar o valor numérico tratado

---

### send_email()

Responsável por:

- Abrir o Gmail
- Criar uma nova mensagem
- Inserir destinatário e conteúdo
- Acionar o envio

---

## Tecnologias utilizadas

- Python  
- Tkinter  
- Playwright  
- Regex  

---

## Padrões adotados

- Separação de responsabilidades por função
- Uso de logs para rastreamento
- Validação de entradas do usuário

---

## Possíveis melhorias no código

- Implementação de testes automatizados
- Modularização em arquivos separados
- Uso de APIs para envio de e-mail
- Tratamento de exceções mais robusto