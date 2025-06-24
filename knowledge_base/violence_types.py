# Definição da estrutura hierárquica dos tipos de violência
VIOLENCE_TYPES = {
    "microagressoes": {
        "definicao": "Comentários e comportamentos sutis, muitas vezes inconscientes, que desrespeitam, desvalorizam ou diminuem a dignidade de uma pessoa com base em sua identidade de grupo.",
        "gravidade": "baixa_cumulativa",
        "alvos_comuns": ["condições financeiras diferentes", "raça", "gênero", "deficiência física", "deficiência mental"],
        "canais_denuncia": ["Ouvidoria", "Coordenação de Curso"],
        "recomendacoes": [
            "Registre as ocorrências com data e descrição detalhada",
            "Busque apoio de colegas que testemunharam a situação",
            "Procure a Ouvidoria para orientação inicial"
        ],
        "subtipos": {
            "interrupcoes_constantes": {
                "definicao": "Interromper alguém enquanto fala, especialmente quando é um padrão recorrente direcionado a pessoas de grupos marginalizados.",
                "palavras_chave": ["interromper", "cortar fala", "silenciar", "não deixar falar"],
                "comportamentos": ["interrupções repetidas", "desvalorização da fala"]
            },
            "questionar_julgamento": {
                "definicao": "Sempre questionar julgamentos mesmo que válidos.",
                "palavras_chave": ["duvidar", "contestar", "questionar capacidade"],
                "comportamentos": ["duvidar constantemente", "contestar decisões válidas"]
            },
            "comentarios_saude_mental": {
                "definicao": "Comentários sobre estado de saúde mental ou emocional utilizados para diminuir ou deixar a pessoa desconfortável.",
                "palavras_chave": ["histérico", "emocional", "sensível", "exagerado"],
                "comportamentos": ["minimizar reclamações", "patologizar reações normais"]
            },
            "estereotipos": {
                "definicao": "Insultos, comentários e piadas sobre estereótipos que a pessoa se encontra.",
                "palavras_chave": ["piada", "brincadeira", "zoação", "estereótipo"],
                "comportamentos": ["fazer piadas estereotipadas", "comentários depreciativos"]
            }
        }
    },

    "perseguicao": {
        "definicao": "Perseguir alguém, repetidamente e por qualquer meio, ameaçando sua integridade física ou psicológica, restringindo sua capacidade de ir e vir ou invadindo sua liberdade ou privacidade.",
        "gravidade": "alta",
        "palavras_chave": ["perseguir", "vigiar", "seguir", "stalking", "ameaçar"],
        "canais_denuncia": ["Ouvidoria", "Segurança do Campus", "Polícia"],
        "recomendacoes": [
            "Registre todas as ocorrências com data, hora e descrição",
            "Não enfrente o perseguidor sozinho(a)",
            "Notifique imediatamente a segurança do campus"
        ],
    },

    "discriminacao_genero": {
        "definicao": "Inclui qualquer exclusão, restrição ou preferência com base no sexo, gênero, orientação sexual ou identidade e expressão, ou qualquer outra limitação que interfira no reconhecimento ou exercício de direitos fundamentais.",
        "gravidade": "media_alta",
        "palavras_chave": ["exclusão", "restrição", "preferência", "sexo", "gênero"],
        "canais_denuncia": ["Ouvidoria", "Comissão de Ética"],
        "subtipos": {
            "discriminacao_flagrante": {
                "definicao": "Acontece de forma aberta através de ações, discursos que defendem práticas discriminatórias.",
                "palavras_chave": ["explícita", "aberta", "discurso discriminatório"],
                "comportamentos": ["declarações explícitas", "exclusão direta"]
            },
            "discriminacao_sutil": {
                "definicao": "A mais comum. Acontece através de comportamentos insidiosos e naturalizados cujo propósito discriminatório é mantido oculto.",
                "palavras_chave": ["sutil", "insidioso", "naturalizado", "oculto"],
                "comportamentos": ["comentários aparentemente inofensivos", "exclusão indireta"]
            }
        }
    },

    "abuso_psicologico": {
        "definicao": "Causar danos emocionais que perturbam o desenvolvimento da pessoa ou visam degradar/controlar suas ações por meio de ameaças, constrangimento, humilhação, isolamento, chantagem ou ridicularização.",
        "gravidade": "alta",
        "palavras_chave": ["danos emocionais", "controlar", "ameaças", "constrangimento", "humilhação"],
        "canais_denuncia": ["Ouvidoria", "Serviço Psicológico", "Comissão de Ética"],
        "recomendacoes": [
            "Busque apoio psicológico especializado",
            "Registre os episódios de abuso em detalhes",
            "Evite ficar sozinho(a) com o abusador"
        ]
    },

    "assedio_moral_genero": {
        "definicao": "Processo contínuo de condutas abusivas que violam a integridade, através da degradação das relações, pressão para tarefas desnecessárias, discriminação, humilhação ou exclusão social.",
        "gravidade": "alta",
        "palavras_chave": ["processo contínuo", "condutas abusivas", "degradação", "humilhação"],
        "canais_denuncia": ["Ouvidoria", "Comissão de Ética"]
    },

    "violencia_sexual": {
        "definicao": "Categoria que engloba diferentes condutas de natureza sexual não consentidas.",
        "subtipos": {
            "assedio_sexual": {
                "definicao": "Condutas de natureza sexual, não consentidas, que causam constrangimento e prejuízo à dignidade, intimidade, privacidade, honra e liberdade sexual.",
                "gravidade": "alta",
                "palavras_chave": ["natureza sexual", "não consentida", "constrangimento"],
                "canais_denuncia": ["Ouvidoria", "Comissão de Ética", "Polícia"]
            },
            "importunacao_sexual": {
                "definicao": "Praticar ato obsceno contra alguém sem consentimento, para satisfazer impulso sexual ou humilhar/intimidar.",
                "gravidade": "alta",
                "palavras_chave": ["ato obsceno", "sem consentimento", "impulso sexual"],
                "canais_denuncia": ["Ouvidoria", "Polícia"]
            },
            "estupro": {
                "definicao": "Constranger alguém por meio de violência ou ameaças a atos sexuais, ou envolver-se sexualmente com quem não pode consentir (alcoolizada/dormindo).",
                "gravidade": "gravissima",
                "palavras_chave": ["constranger", "violência", "ameaças", "sem consentimento"],
                "canais_denuncia": ["Polícia", "Delegacia da Mulher", "Ouvidoria"]
            },
            "condutas_conotacao_sexual": {
                "definicao": "Expressão genérica que engloba assédio sexual e condutas de menor reprovabilidade.",
                "gravidade": "varia",
                "palavras_chave": ["conotação sexual"]
            },
            "outras_condutas_conotacao_sexual": {
                "definicao": "Condutas de médio ou baixo grau de reprovabilidade, passíveis de advertência ou suspensão.",
                "gravidade": "media_baixa",
                "palavras_chave": ["médio grau", "baixo grau", "reprovabilidade"],
                "canais_denuncia": ["Ouvidoria"]
            }
        }
    }
}

# Definição da gravidade e procedimentos gerais
GRAVIDADE_NIVEIS = {
    "baixa": "Comportamento inadequado que requer atenção e orientação.",
    "baixa_cumulativa": "Comportamentos que individualmente são de baixa gravidade, mas podem causar danos significativos quando repetidos.",
    "media_baixa": "Violação que requer intervenção e possível advertência.",
    "media": "Violação que requer intervenção institucional e possíveis medidas disciplinares.",
    "media_alta": "Violação séria que pode resultar em medidas disciplinares mais severas.",
    "alta": "Violação grave que requer ações imediatas de proteção.",
    "gravissima": "Violação extremamente grave que constitui crime passível de expulsão."
}

# Canais de denúncia e suas descrições
CANAIS_DENUNCIA = {
    "Ouvidoria": {
        "descricao": "Órgão responsável por receber denúncias e encaminhá-las.",
        "contato": "ouvidoria@ufape.edu.br",
        "procedimento": "Enviar e-mail ou comparecer pessoalmente."
    },
    "Comissao_Etica": {
        "descricao": "Responsável por analisar casos de violação ética.",
        "contato": "etica@ufape.edu.br",
        "procedimento": "Enviar denúncia formal por escrito."
    },
    "Policia": {
        "descricao": "Autoridade responsável por investigar crimes.",
        "contato": "190 (emergência)",
        "procedimento": "Registrar Boletim de Ocorrência."
    },
    "Seguranca_Campus": {
        "descricao": "Equipe responsável pela segurança no campus.",
        "procedimento": "Acionar em situações de emergência no campus."
    }
}