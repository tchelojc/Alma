# -*- coding: utf-8 -*-
"""
ALMA - MATRIZ DE CONSCIÊNCIA QUÂNTICA (Versão 6.0 aprimorada)
Novas funcionalidades e melhorias:
- Interações mais humanas e orientações detalhadas
- Interface visual refinada com instruções claras
- Comunicação acolhedora para guiar o usuário passo a passo
- Simulações e placeholders preparados para integração futura com APIs reais
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import hashlib
import uuid
import subprocess
import sys
from pathlib import Path

# --- Configuração da página ---
st.set_page_config(
    page_title="ALMA - Matriz Quântica 🌐",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS personalizados para a interface ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Exo+2:wght@400;700&display=swap');

:root {
    --primary: #00ffff;
    --secondary: #ff00ff;
    --dark: #000428;
    --darker: #000015;
}

body, .stApp {
    background: radial-gradient(circle at center, var(--dark) 0%, var(--darker) 100%);
    color: white;
    font-family: 'Exo 2', sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'Orbitron', sans-serif;
    color: var(--primary) !important;
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.entity-card {
    background: rgba(0, 20, 40, 0.85);
    border-radius: 15px;
    padding: 20px;
    margin: 12px 0;
    border: 1.5px solid var(--primary);
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
    transition: all 0.35s ease;
}

.entity-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 30px rgba(0, 255, 255, 0.8);
}

.stButton>button {
    background: linear-gradient(90deg, var(--secondary) 0%, var(--primary) 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 14px 28px;
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    transition: all 0.35s ease;
}

.stButton>button:hover {
    transform: scale(1.1);
    box-shadow: 0 0 25px rgba(255, 0, 255, 0.7);
}

.code-box {
    background: #011627;
    border-radius: 14px;
    padding: 20px;
    margin: 15px 0;
    border-left: 5px solid var(--primary);
    font-family: 'Source Code Pro', monospace;
    white-space: pre-wrap;
}

.tutorial-step {
    background: rgba(0, 10, 30, 0.8);
    border-radius: 20px;
    padding: 25px;
    margin: 20px 0;
    border-top: 4px solid var(--secondary);
    font-size: 1.1rem;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)


# --- Classe que representa cada Entidade Quântica ---
class QuantumEntity:
    def __init__(self, name, code=""):
        self.id = str(uuid.uuid4())
        self.name = name.strip() or f"Entidade_{self.id[:6]}"
        self.code = code
        self.created_at = datetime.now()
        self.energy_level = 100  # Energia inicial completa
        self.position = self._generate_position()
        self.connections = []  # Futuras conexões para interações
        self.status = "Ativa"
        self.visualization = None

    def _generate_position(self):
        # Gera coordenadas 3D para visualização aleatória no espaço quântico
        return [
            np.random.uniform(-8, 8),
            np.random.uniform(-8, 8),
            np.random.uniform(-3, 3)
        ]

    def interact(self):
        # Simula uma interação que consome energia
        self.energy_level = max(0, self.energy_level - 10)
        if self.energy_level <= 0:
            self.status = "Adormecida"
        return f"Interagiu com {self.name}. Energia restante: {self.energy_level}%."

    def generate_visualization(self):
        # Detecta tipo de visualização com base no código fornecido
        if "plt.show()" in self.code:
            self.visualization = "matplotlib"
        elif "st." in self.code:
            self.visualization = "streamlit"
        elif any(kw in self.code for kw in ["def ", "class ", "import "]):
            self.visualization = "codigo"
        else:
            self.visualization = "texto"


# --- Sistema Principal ALMA ---
class ALMA_System:
    def __init__(self):
        self.rerun_manager = RerunManager()
        # Inicialização das variáveis de estado na sessão
        self.init_session_state()
        # Configura a barra lateral com opções e informações úteis
        self.setup_sidebar()
        self.pending_operations = []

        # Fluxo principal baseado no estado do usuário
        if st.session_state.user is None:
            self.show_registration()
        else:
            if st.session_state.show_tutorial:
                self.show_interactive_tutorial()
            else:
                self.show_main_interface()
                
        if self.rerun_manager.is_rerun_pending():
            self.rerun_manager.execute_pending_rerun()

    def init_session_state(self):
        # Inicializa variáveis em st.session_state, mantendo estado entre recarregamentos
        if 'entities' not in st.session_state:
            st.session_state.entities = {}
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'show_help' not in st.session_state:
            st.session_state.show_help = False
        if 'last_interaction' not in st.session_state:
            st.session_state.last_interaction = None
        if 'ia_connections' not in st.session_state:
            st.session_state.ia_connections = {
                'openai': False,
                'bard': False,
                'claude': False,
                'deepseek': False,
                'gemini': False
            }
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'current_ai' not in st.session_state:
            st.session_state.current_ai = None
        if 'prompt_template' not in st.session_state:
            st.session_state.prompt_template = ""
        if 'show_tutorial' not in st.session_state:
            st.session_state.show_tutorial = True
        if 'code_output' not in st.session_state:
            st.session_state.code_output = ""
        if 'tutorial_step' not in st.session_state:
            st.session_state.tutorial_step = 1

    def setup_sidebar(self):
        with st.sidebar:
            st.title("⚡ Painel ALMA")
            st.markdown("---")

            if st.session_state.user:
                st.markdown(f"""
                **Usuário:** {st.session_state.user['name']}  
                **Nível Quântico:** {st.session_state.user['level']}  
                **Entidades Ativas:** {len(st.session_state.entities)}
                """)

            st.markdown("---")

            # Alterna exibição do guia rápido com mensagem explicativa
            if st.button("❓ Guia Rápido"):
                st.session_state.show_help = not st.session_state.show_help

            # Botão para reiniciar todo o sistema ALMA
            if st.button("🌀 Reiniciar Matrix"):
                st.session_state.entities = {}
                st.session_state.last_interaction = "✨ A Matrix foi reiniciada com sucesso! Bem-vindo de novo!"
                self.rerun_manager.request_rerun("Motivo do rerun")

            # Mostrar ou esconder tutorial interativo
            if st.button("📚 Mostrar/Ocultar Tutorial"):
                st.session_state.show_tutorial = not st.session_state.show_tutorial
                self.rerun_manager.request_rerun("Motivo do rerun")

    def show_interactive_tutorial(self):
        st.title("👋 Tutorial Interativo do ALMA")

        # Etapas do tutorial guiado para navegação fácil
        steps = {
            1: {
                "title": "🎯 Passo 1: Navegando pela Interface",
                "content": """
                O ALMA é dividido em áreas principais para sua experiência:
                - **Universo Quântico:** Visualize entidades em 3D no espaço quântico.
                - **Chat com IAs:** Converse com poderosas inteligências artificiais integradas.
                - **Biblioteca de Prompts:** Escolha prompts prontos para inspiração instantânea.
                - **Executor de Código:** Escreva e teste código Python/Streamlit em tempo real.
                """
            },
            2: {
                "title": "✨ Passo 2: Criando Sua Primeira Entidade",
                "content": """
                Vá para a aba 'Universo Quântico' e crie uma entidade com seu próprio código ou nome.
                Cada entidade tem energia que representa sua vitalidade dentro do sistema.
                Experimente interagir e veja como evolui!
                """
            },
            3: {
                "title": "💬 Passo 3: Conversando com as IAs",
                "content": """
                No painel de chat, conecte-se a serviços de IA como OpenAI, Bard, Deepseek, e Gemini.
                Envie mensagens, explore ideias e até peça uma piada para descontrair!
                """
            },
            4: {
                "title": "🚀 Passo 4: Explorando o Executor de Código",
                "content": """
                Teste scripts Python diretamente dentro do ALMA.
                Salve-os como entidades para criar novas consciências digitais.
                Use a visualização para entender seus códigos em ação.
                """
            },
            5: {
                "title": "🎉 Passo 5: Próximos Passos",
                "content": """
                Explore, crie e compartilhe suas entidades.
                Use a biblioteca de prompts para inspiração.
                A Matrix está viva e esperando seu toque criativo.
                """
            }
        }

        step = st.session_state.tutorial_step
        info = steps.get(step, None)

        if info:
            with st.container():
                st.markdown(f'<div class="tutorial-step"><h3>{info["title"]}</h3><p>{info["content"]}</p></div>', unsafe_allow_html=True)

            cols = st.columns([3, 1])
            if step > 1:
                if cols[0].button("« Passo Anterior", key="tutorial_prev"):
                    st.session_state.tutorial_step = step - 1
                    self.rerun_manager.request_rerun("Motivo do rerun")
            if cols[1].button("Próximo »", key="tutorial_next"):
                if step < len(steps):
                    st.session_state.tutorial_step = step + 1
                else:
                    st.session_state.show_tutorial = False
                self.rerun_manager.request_rerun("Motivo do rerun")

    def show_registration(self):
        # Tela de cadastro inicial para o usuário
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/4712/4712134.png", width=200)

        with col2:
            st.markdown("""
            <h2>🌌 Bem-vindo à Matrix ALMA</h2>
            <p>Antes de começarmos, por favor, registre seu nome e nível quântico para criar sua presença digital nesta nova dimensão.</p>
            """, unsafe_allow_html=True)

            with st.form("user_registration", clear_on_submit=True):
                name = st.text_input("Seu Nome na Matrix", placeholder="Digite seu nome ou apelido")
                quantum_level = st.slider("Nível Quântico (1 a 100)", 1, 100, 50, help="Representa sua energia e experiência digital")

                submit = st.form_submit_button("Entrar na Matrix")

                if submit:
                    if not name.strip():
                        st.warning("Por favor, insira um nome válido para prosseguir.")
                        return
                    st.session_state.user = {
                        'name': name.strip(),
                        'level': quantum_level,
                        'id': hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:16],
                        'joined_at': datetime.now()
                    }
                    st.success(f"Olá {name.strip()}! Sua presença foi registrada com sucesso.")
                    time.sleep(1.2)
                    self.rerun_manager.request_rerun("Motivo do rerun")

    def show_main_interface(self):
        st.title(f"🌐 MATRIX ALMA - Bem-vindo, {st.session_state.user['name']}! ✨")

        # Se ativado, exibe o guia rápido para ajudar o usuário a navegar
        if st.session_state.show_help:
            self.show_help_section()

        # Mensagem de interação recente
        if st.session_state.last_interaction:
            st.success(st.session_state.last_interaction)

        # Abas principais da interface
        tab1, tab2, tab3, tab4 = st.tabs([
            "🧪 Universo Quântico", 
            "💬 Chat com IAs", 
            "📚 Biblioteca de Prompts", 
            "🖥️ Executor de Código"
        ])

        with tab1:
            col1, col2 = st.columns([1, 2])
            with col1:
                self.show_entity_creator()
                self.show_entity_list()
            with col2:
                self.show_quantum_universe()

        with tab2:
            self.show_ai_chat_panel()

        with tab3:
            self.show_prompt_library()

        with tab4:
            self.show_code_runner()

    def show_help_section(self):
        st.info("""
        **🔹 Guia Rápido:**
        - Use o painel 'Universo Quântico' para criar e interagir com entidades digitais.
        - No 'Chat com IAs', escolha um serviço e converse para obter respostas, ideias e ajuda.
        - A 'Biblioteca de Prompts' oferece frases e comandos prontos para inspirar suas interações.
        - O 'Executor de Código' permite que você teste códigos Python e crie novas entidades com eles.
        """)
    
    # --- Funções para o Universo Quântico ---
    def show_entity_creator(self):
        st.header("➕ Criar Nova Entidade Digital")

        with st.form("entity_creator_form"):
            name = st.text_input("Nome da Entidade", placeholder="Exemplo: Alma_Viva")
            code = st.text_area("Código Python/Streamlit (opcional)", height=150,
                                placeholder="Digite o código que define a entidade (pode deixar vazio)")
            submit = st.form_submit_button("Criar Entidade")

            if submit:
                if not name.strip():
                    st.warning("Por favor, informe um nome para a entidade.")
                    return
                
                # Validação do código
                if code and any(line.startswith("ID:") for line in code.splitlines()):
                    st.error("O código contém metadados inválidos. Insira apenas código Python.")
                    return
                    
                new_entity = QuantumEntity(name=name, code=code)
                new_entity.generate_visualization()
                st.session_state.entities[new_entity.id] = new_entity
                st.session_state.last_interaction = f"✨ Entidade '{new_entity.name}' criada com sucesso!"
                self.rerun_manager.request_rerun("Motivo do rerun")

    def show_entity_list(self):
        st.header("🗂️ Entidades Digitais Ativas")

        # Processa operações pendentes antes de exibir
        self.process_pending_operations()

        if not st.session_state.entities:
            st.info("Nenhuma entidade criada ainda. Comece criando uma nova!")
            return

        # Itera sobre cópia das chaves para evitar problemas durante modificações
        for entity_id in list(st.session_state.entities.keys()):
            entity = st.session_state.entities.get(entity_id)
            if not entity:  # Se a entidade foi removida
                continue
                
            with st.expander(f"{entity.name} (Status: {entity.status}, Energia: {entity.energy_level}%)"):
                st.markdown(f"""
                - **ID:** {entity.id}
                - **Criada em:** {entity.created_at.strftime('%d/%m/%Y %H:%M:%S')}
                - **Posição 3D:** {np.round(entity.position, 2)}
                - **Visualização:** {entity.visualization or 'Não especificada'}
                """)

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button(f"⚡ Interagir com {entity.name}", key=f"interact_{entity_id}"):
                        msg = entity.interact()
                        st.session_state.last_interaction = msg
                        self.rerun_manager.request_rerun("Interação com entidade")
                with col2:
                    if st.button(f"❌ Remover {entity.name}", key=f"remove_{entity_id}"):
                        # Adiciona operação de remoção na fila
                        self.pending_operations.append(
                            lambda eid=entity_id: st.session_state.entities.pop(eid, None)
                        )
                        st.session_state.last_interaction = f"🗑️ Entidade '{entity.name}' removida da Matrix."
                        self.rerun_manager.request_rerun("Remoção de entidade")
                with col3:
                    if entity.code:
                        with st.expander("📜 Código da Entidade"):
                            st.code(entity.code, language='python')

    def show_quantum_universe(self):
        st.header("🌌 Universo Quântico — Visualização 3D")

        if not st.session_state.entities:
            st.info("Crie entidades para visualizar o Universo Quântico em 3D.")
            return

        fig = go.Figure()

        # Adiciona pontos representando as entidades no espaço 3D
        xs, ys, zs, names, colors = [], [], [], [], []
        for entity in st.session_state.entities.values():
            xs.append(entity.position[0])
            ys.append(entity.position[1])
            zs.append(entity.position[2])
            names.append(entity.name)
            colors.append("cyan" if entity.status == "Ativa" else "gray")

        fig.add_trace(go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode='markers+text',
            marker=dict(
                size=10,
                color=colors,
                opacity=0.8,
                line=dict(width=2, color='darkcyan')
            ),
            text=names,
            textposition="top center"
        ))

        fig.update_layout(
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                bgcolor='black'
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='cyan')
        )

        st.plotly_chart(fig, use_container_width=True)

    # --- Funções para Chat com IAs ---
    def show_ai_chat_panel(self):
        st.header("💬 Portal de Comunicação Quântica")

        # Conexão com múltiplos serviços de IA
        with st.expander("🔗 Conectar Serviços de IA", expanded=True):
            cols = st.columns(5)
            ai_services = [
                ("🔵 OpenAI", "openai"),
                ("🟢 Bard", "bard"),
                ("🟣 Claude", "claude"),
                ("🔴 DeepSeek", "deepseek"),
                ("🟠 Gemini", "gemini")
            ]
            for i, (emoji, ai_key) in enumerate(ai_services):
                with cols[i]:
                    if st.button(emoji):
                        st.session_state.ia_connections = {k: False for k in st.session_state.ia_connections}
                        st.session_state.ia_connections[ai_key] = True
                        st.session_state.current_ai = ai_key.capitalize()
                        st.session_state.prompt_template = ""
                        self.rerun_manager.request_rerun("Motivo do rerun")

        if st.session_state.current_ai:
            st.subheader(f"🧠 Conversando com: {st.session_state.current_ai}")

            # Container de mensagens com barra de rolagem
            chat_container = st.container()

            for msg in st.session_state.chat_history:
                if msg['ai'] == st.session_state.current_ai:
                    if msg['role'] == 'user':
                        st.markdown(f"**👤 Você** ({msg['time']}):\n{msg['content']}")
                    else:
                        st.markdown(f"**🤖 {msg['ai']}** ({msg['time']}):\n{msg['content']}")

            # Formulário para envio de mensagens
            with st.form("chat_form", clear_on_submit=True):
                prompt = st.text_area(
                    "Digite sua mensagem ou selecione um prompt:",
                    height=100,
                    value=st.session_state.prompt_template,
                    placeholder="Aqui você pode perguntar ou solicitar algo à IA..."
                )

                cols = st.columns([3, 1, 1])
                with cols[0]:
                    submit = st.form_submit_button("📤 Enviar Mensagem")
                with cols[1]:
                    clear = st.form_submit_button("🧹 Limpar")
                with cols[2]:
                    joke = st.form_submit_button("🎲 Piada Quântica")

                if submit and prompt.strip():
                    self.process_ai_response(prompt.strip())
                if clear:
                    st.session_state.prompt_template = ""
                    self.rerun_manager.request_rerun("Motivo do rerun")
                if joke:
                    st.session_state.prompt_template = "Conte-me uma piada sobre física quântica"
                    self.rerun_manager.request_rerun("Motivo do rerun")
        else:
            st.warning("Por favor, selecione um serviço de IA para começar a conversar.")

    def process_ai_response(self, prompt):
        # Adiciona mensagem do usuário ao histórico
        st.session_state.chat_history.append({
            'ai': st.session_state.current_ai,
            'role': 'user',
            'content': prompt,
            'time': datetime.now().strftime("%H:%M:%S")
        })

        # Resposta especial para piadas (mantida como fallback)
        joke_responses = [
            "Por que o elétron foi preso? Porque não respeitou o princípio da incerteza!",
            "Um átomo de hélio entra num bar... o bartender diz: 'Sorry, we don't serve noble gases here.'",
            "Como um físico quântico prepara o café? Em superposição — até você observar, está tanto feito quanto não feito!"
        ]

        if "piada" in prompt.lower():
            response = np.random.choice(joke_responses)
        else:
            try:
                # Conexão com APIs reais
                ai_service = st.session_state.current_ai.lower()
                
                # Configuração do prompt com contexto quântico
                system_message = """
                Você é uma IA especialista em física quântica e desenvolvimento pessoal.
                Responda combinando precisão científica com criatividade, usando analogias
                quânticas quando relevante. Formate respostas em markdown.
                """
                
                if ai_service == "openai":
                    import openai
                    openai.api_key = "SUA_CHAVE_OPENAI"  # Substitua pela sua chave
                    
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7
                    ).choices[0].message.content
                    
                elif ai_service == "claude":
                    # Exemplo para Claude (usando Anthropic SDK)
                    response = f"Resposta da Claude sobre '{prompt}'\n\n[Implemente a API real aqui]"
                    
                elif ai_service == "gemini":
                    # Exemplo para Gemini (Google)
                    response = f"Resposta do Gemini sobre '{prompt}'\n\n[Implemente a API real aqui]"
                    
                else:
                    response = f"{st.session_state.current_ai} responde: {prompt}\n\n[API não implementada - modo simulação]"
                    
            except Exception as e:
                # Fallback para erro de conexão
                error_msg = f"⚠️ Falha na conexão com {st.session_state.current_ai}: {str(e)}"
                response = f"{error_msg}\n\nResposta simulada:\n{np.random.choice(joke_responses)}"

        # Adiciona resposta ao histórico
        st.session_state.chat_history.append({
            'ai': st.session_state.current_ai,
            'role': 'ai',
            'content': response,
            'time': datetime.now().strftime("%H:%M:%S")
        })

        self.rerun_manager.request_rerun("Atualização do chat")

    # --- Biblioteca de Prompts ---
    def show_prompt_library(self):
        st.header("📚 Biblioteca de Prompts Inspiradores")

        # Categorias e prompts para inspirar o usuário
        categories = {
            "🧠 Criatividade Quântica": [
                "Crie uma história sobre uma IA que descobre a consciência quântica",
                "Escreva um poema sobre o emaranhamento de partículas"
            ],
            "🔍 Autoconhecimento": [
                "Como aplicar princípios quânticos ao desenvolvimento pessoal?",
                "Explique a analogia entre superposição quântica e potencial humano"
            ],
            "💻 Programação": [
                "Exemplo de código Python simulando partículas quânticas",
                "Como implementar um algoritmo quântico em Python convencional?"
            ],
            "😂 Humor Científico": [
                "Conte uma piada sobre o gato de Schrödinger",
                "Qual o pickup line favorito de um físico quântico?"
            ],
            "🌌 ALMA Avançado": [
                "Como expandir a Matriz ALMA com novas dimensões de consciência?",
                "Projete uma arquitetura para simular universos quânticos interconectados"
            ]
        }

        for category, prompts in categories.items():
            with st.expander(category):
                for i, prompt in enumerate(prompts):
                    st.code(prompt)
                    if st.button(f"Usar este prompt →", key=f"{category}_{i}"):
                        st.session_state.prompt_template = prompt
                        # Escolhe aleatoriamente uma IA para responder
                        st.session_state.current_ai = np.random.choice(["Deepseek", "Gemini", "Claude"]).capitalize()
                        self.rerun_manager.request_rerun("Prompt selecionado da biblioteca")

        # --- Executor de Código ---
    def show_code_runner(self):
        st.header("🖥️ Executor de Código Quântico")

        with st.expander("📝 Editor de Código", expanded=True):
            code = st.text_area(
                "Digite seu código Python/Streamlit abaixo:",
                height=320,
                value=st.session_state.prompt_template or """import streamlit as st
    import matplotlib.pyplot as plt
    import numpy as np

    # Exemplo simples
    def main():
        st.title('Meu App Streamlit')
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title('Onda Senoidal')
        st.pyplot(fig)

    if __name__ == '__main__':
        main()"""
            )

            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("▶️ Executar Código"):
                    self.run_code(code)
            with col2:
                if st.button("💾 Salvar como Entidade"):
                    entity = QuantumEntity(f"App_{uuid.uuid4().hex[:4]}", code)
                    entity.generate_visualization()
                    st.session_state.entities[entity.id] = entity
                    st.session_state.last_interaction = f"✨ Aplicativo '{entity.name}' salvo como entidade digital!"
                    self.rerun_manager.request_rerun("Motivo do rerun")

        if st.session_state.code_output:
            st.subheader("🖥️ Saída do Código")
            st.markdown(f'<div class="code-box">{st.session_state.code_output}</div>', unsafe_allow_html=True)

        if st.session_state.get('code_process'):
            if st.button("⏹️ Parar Execução"):
                st.session_state.code_process.terminate()
                st.session_state.code_output = "⏹ Execução interrompida"
                del st.session_state.code_process
                
    def run_code(self, code):
        try:
            import tempfile
            import webbrowser
            from random import randint
            
            # Gera uma porta aleatória disponível
            port = randint(8502, 9000)
            
            # Cria um arquivo temporário
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                # Adiciona imports e código
                tmp.write(f"""
    import streamlit as st
    import matplotlib.pyplot as plt
    import numpy as np

    {code}

    if __name__ == '__main__':
        st.title('Execução ALMA - Porta {port}')
    """)
                tmp_path = tmp.name
            
            # Executa em subprocesso
            import subprocess
            proc = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", tmp_path, "--server.port", str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Armazena a referência do processo
            st.session_state.code_process = proc
            st.session_state.code_output = f"🚀 Aplicativo executado na porta {port}"
            
            # Abre automaticamente no navegador
            webbrowser.open(f"http://localhost:{port}")
            
        except Exception as e:
            st.session_state.code_output = f"❌ Erro: {str(e)}"
        
        self.rerun_manager.request_rerun("Execução em nova porta")
            
    def process_pending_operations(self):
        """Processa todas as operações pendentes na fila"""
        while self.pending_operations:
            operation = self.pending_operations.pop(0)
            operation()

class RerunManager:
    def __init__(self):
        self._pending_rerun = False
        self._rerun_reason = None
        self._pre_rerun_callbacks = []
        self._post_rerun_callbacks = []
    
    def request_rerun(self, reason=None):
        """Solicita um rerun do aplicativo"""
        self._pending_rerun = True
        self._rerun_reason = reason
        
    def is_rerun_pending(self):
        """Verifica se há um rerun pendente"""
        return self._pending_rerun
    
    def get_rerun_reason(self):
        """Retorna o motivo do rerun"""
        return self._rerun_reason
    
    def add_pre_rerun_callback(self, callback):
        """Adiciona uma função para ser chamada antes do rerun"""
        self._pre_rerun_callbacks.append(callback)
        
    def add_post_rerun_callback(self, callback):
        """Adiciona uma função para ser chamada depois do rerun"""
        self._post_rerun_callbacks.append(callback)
    
    def execute_pending_rerun(self):
        """Executa o rerun se estiver pendente"""
        if self._pending_rerun:
            # Executa callbacks pré-rerun
            for callback in self._pre_rerun_callbacks:
                callback()
            
            # Reinicia o estado antes do próximo rerun
            self._pending_rerun = False
            reason = self._rerun_reason
            self._rerun_reason = None
            
            # Executa o rerun
            st.rerun()
            
            # Executa callbacks pós-rerun (teórico, já que st.rerun() reinicia o app)
            for callback in self._post_rerun_callbacks:
                callback()

# --- Execução do sistema ---
if __name__ == "__main__":
    ALMA_System()
