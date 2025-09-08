# Valorant Spike Timer

Este é um temporizador de spike de Valorant simples e leve, criado com Python e as bibliotecas Pygame e Tkinter. O objetivo do projeto é oferecer uma ferramenta prática para ajudar jogadores a gerenciar o tempo da spike de forma eficiente, melhorando a tomada de decisões durante as rodadas.

---

### Por que usar?

O Valorant Spike Timer foi desenvolvido com foco total na segurança do jogador. Você pode usá-lo sem se preocupar em ser banido, e aqui está o motivo:

1.  **Não interfere com o jogo:** Este aplicativo não lê, injeta ou modifica nenhum dado do cliente do jogo Valorant. Ele funciona como uma ferramenta externa e independente, baseada em tempo real.
2.  **Não utiliza a API do jogo:** A Riot Games, desenvolvedora do Valorant, oferece uma API para desenvolvedores de terceiros. No entanto, ela não fornece dados de tempo da partida em tempo real, como o momento em que a spike é plantada. Nosso aplicativo contorna essa limitação usando um temporizador manual, ativado pelo usuário.
3.  **Totalmente manual:** A contagem do tempo da spike é iniciada manualmente por você, através de uma tecla de atalho. Isso significa que a ferramenta não automatiza nenhuma ação do jogo. Ela é apenas um auxílio visual para o jogador.

Ferramentas que interagem diretamente com o cliente do jogo ou que automatizam ações podem levar a banimentos, mas este temporizador não faz nada disso. Ele é seguro porque o controle está sempre nas mãos do jogador.

---

### Funcionalidades

- **Temporizador Preciso:** Inicie a contagem regressiva de 45 segundos da spike com uma tecla de atalho.
- **Controle Visual:** A spike na tela muda de cor (de verde para vermelho) e pisca gradualmente mais rápido conforme o tempo acaba, oferecendo um alerta visual claro.
- **Controle por Botão:** Inicie e pare o temporizador também com botões na interface.
- **Piscar Customizável:** Uma opção para ativar ou desativar o efeito de piscar da spike.
- **Tempo Definível:** Um campo de texto para definir um tempo de spike customizado, útil para treinos ou modos de jogo específicos.
- **Configuração de Atalho:** Mude a tecla de atalho facilmente através de um modo de configuração intuitivo.
- **Janelas Centralizadas:** A caixa de diálogo "Sobre" e a tela de configuração de tempo são centralizadas na janela do aplicativo, proporcionando uma experiência de usuário mais agradável.

---

### Como Usar

1.  **Baixe** todos os arquivos do projeto para uma mesma pasta.
2.  **Abra o Terminal** e instale as bibliotecas necessárias:
    ```bash
    pip install pygame pillow keyboard
    ```
3.  **Execute o programa:**
    ```bash
    python main.py
    ```
4.  **No jogo,** use a tecla de atalho configurada (padrão: `F1`) para iniciar e parar o temporizador.

---

### Autor

**Luiz F. R. Pimentel**

- [GitHub](https://github.com/KanekiZLF)
