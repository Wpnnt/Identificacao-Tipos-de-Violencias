# Pesos para critérios de pontuação (movido de confidence_levels.py)
CRITERION_WEIGHTS = {
    "behavior": {
        "critical": 10,    # Comportamento crítico/determinante
        "relevant": 7,     # Comportamento relevante
        "supporting": 4    # Comportamento suportivo
    },
    "frequency": {
        "single": 2,           # Uma única vez
        "few": 4,              # Algumas vezes
        "repeated": 6,         # Repetidamente
        "continuous": 8        # Continuamente
    },
    "context": {
        "critical": 10,    # Contexto determinante (ex: local de trabalho para assédio moral)
        "relevant": 5,     # Contexto relevante
        "supporting": 2    # Contexto menos relevante
    },
    "target": {
        "critical": 10,    # Característica determinante
        "relevant": 7,     # Característica relevante
        "supporting": 3    # Característica complementar
    },
    "impact": {
        "critical": 9,     # Impacto determinante
        "strong": 7,       # Impacto forte
        "moderate": 4,     # Impacto moderado
        "mild": 2          # Impacto leve
    },
    "relationship": {
        "hierarchical": 5, # Relação hierárquica
        "peer": 3,         # Relação entre pares
        "ex_partner": 5,   # Ex-parceiros
        "unknown": 1       # Desconhecido
    }
}

# Definição da estrutura hierárquica dos tipos de violência
VIOLENCE_TYPES = {
    "microagressoes": {
        "definicao": "Comentários e comportamentos sutis, muitas vezes inconscientes, que desrespeitam, desvalorizam ou diminuem a dignidade de uma pessoa com base em sua identidade de grupo.",
        "gravidade": "baixa_cumulativa",
        "alvos_comuns": ["condições financeiras diferentes", "raça", "gênero", "deficiência física", "deficiência mental"],
        "canais_denuncia": ["Ouvidoria", "Coordenação de Curso"],
        "recomendacoes": [
            "Documente cada incidente com data, hora, local e detalhes sobre o que foi dito/feito",
            "Comunique claramente seus limites: 'Esse comentário me faz sentir desconfortável'",
            "Busque apoio em coletivos identitários ou grupos de afinidade na instituição",
            "Converse com colegas que possam ter testemunhado para validar sua experiência",
            "Reporte padrões recorrentes à Ouvidoria institucional ou à Coordenação",
            "Considere abordar o assunto em reuniões departamentais se o problema for sistemático",
            "Preserve sua saúde mental buscando apoio psicológico se necessário"
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
            "Notifique imediatamente autoridades competentes (Segurança do Campus e, em casos graves, a Polícia)",
            "Nunca confronte o perseguidor diretamente ou sozinho(a)",
            "Registre detalhadamente cada ocorrência (datas, horários, locais e descrições)",
            "Preserve todas as evidências: mensagens, e-mails, presentes indesejados",
            "Modifique suas rotinas e trajetos para dificultar a previsibilidade",
            "Informe pessoas próximas sobre a situação para ampliar sua rede de proteção",
            "Solicite medidas protetivas através dos canais institucionais e/ou judiciais",
            "Reporte à Polícia se houver ameaças explícitas ou comportamento intimidador persistente"
        ],
    },

    "discriminacao_genero": {
        "definicao": "Inclui qualquer exclusão, restrição ou preferência com base no sexo, gênero, orientação sexual ou identidade e expressão, ou qualquer outra limitação que interfira no reconhecimento ou exercício de direitos fundamentais.",
        "gravidade": "media_alta",
        "palavras_chave": ["exclusão", "restrição", "preferência", "sexo", "gênero"],
        "canais_denuncia": ["Ouvidoria", "Comissão de Ética"],
        "recomendacoes": [
            "Registre situações discriminatórias com detalhes específicos e nomes de testemunhas",
            "Consulte o núcleo de diversidade ou comissão de igualdade de gênero da instituição",
            "Formalize denúncia à Ouvidoria e à Comissão de Ética institucional",
            "Busque apoio em coletivos feministas ou LGBTQIA+ para orientação e suporte",
            "Informe-se sobre políticas de gênero vigentes na instituição",
            "Considere acompanhamento psicológico para lidar com os impactos emocionais",
            "Em casos de discriminação flagrante e sistemática, considere denúncia ao Ministério Público"
        ],
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
            "Registre detalhadamente os episódios, incluindo data, horário, local e testemunhas",
            "Busque apoio psicológico especializado para processar o trauma e desenvolver estratégias",
            "Evite ficar a sós com a pessoa abusadora em qualquer circunstância",
            "Reporte formalmente à Ouvidoria e à Comissão de Ética da instituição",
            "Solicite transferência de setor/turma se compartilhar ambiente com o abusador",
            "Estabeleça limites claros em todas as interações necessárias",
            "Busque apoio em sua rede social (amigos, família, colegas de confiança)",
            "Reporte à Polícia em casos que envolvam ameaças explícitas à segurança"
        ]
    },

    "assedio_moral_genero": {
        "definicao": "Processo contínuo de condutas abusivas que violam a integridade, através da degradação das relações, pressão para tarefas desnecessárias, discriminação, humilhação ou exclusão social.",
        "gravidade": "alta",
        "palavras_chave": ["processo contínuo", "condutas abusivas", "degradação", "humilhação"],
        "canais_denuncia": ["Ouvidoria", "Comissão de Ética"],
        "recomendacoes": [
            "Documente todas as ocorrências com data, hora, local e descrições precisas",
            "Salve e-mails, mensagens e comunicações que evidenciem o tratamento diferenciado",
            "Procure identificar testemunhas que possam corroborar seu relato",
            "Consulte o setor de recursos humanos ou equivalente sobre políticas de assédio",
            "Acione a Ouvidoria e Comissão de Ética para formalizar denúncia",
            "Busque apoio psicológico para lidar com o estresse e pressão continuados",
            "Considere acompanhamento jurídico especializado em direito trabalhista",
            "Denuncie ao Ministério Público do Trabalho em casos graves e persistentes"
        ]
    },

    "violencia_sexual": {
        "definicao": "Categoria que engloba diferentes condutas de natureza sexual não consentidas.",
        "canais_denuncia": ["Polícia", "Ouvidoria", "Delegacia da Mulher"],
        "recomendacoes": [
            "Busque um ambiente seguro imediatamente",
            "Preserve todas as evidências possíveis",
            "Reporte o incidente às autoridades competentes"
        ],
        "subtipos": {
            "assedio_sexual": {
                "definicao": "Condutas de natureza sexual, não consentidas, que causam constrangimento e prejuízo à dignidade, intimidade, privacidade, honra e liberdade sexual.",
                "gravidade": "alta",
                "palavras_chave": ["natureza sexual", "não consentida", "constrangimento"],
                "canais_denuncia": ["Ouvidoria", "Comissão de Ética", "Polícia"],
                "recomendacoes": [
                    "Registre detalhadamente cada ocorrência com data, hora e descrição precisa",
                    "Reporte imediatamente à Ouvidoria e à Comissão de Ética",
                    "Busque apoio em serviços de atendimento psicológico institucional",
                    "Evite situações de isolamento com o assediador",
                    "Considere denúncia formal aos órgãos competentes da instituição",
                    "Busque orientação jurídica para conhecer todas as possibilidades de ação"
                ]
            },
            "importunacao_sexual": {
                "definicao": "Praticar ato obsceno contra alguém sem consentimento, para satisfazer impulso sexual ou humilhar/intimidar.",
                "gravidade": "alta",
                "palavras_chave": ["ato obsceno", "sem consentimento", "impulso sexual"],
                "canais_denuncia": ["Ouvidoria", "Polícia"],
                "recomendacoes": [
                    "Notifique imediatamente as autoridades de segurança presentes",
                    "Busque ajuda de pessoas próximas para intervir e testemunhar",
                    "Registre Boletim de Ocorrência em delegacia especializada (crime previsto em lei)",
                    "Solicite medidas protetivas contra o agressor",
                    "Preserve evidências como gravações, mensagens ou relatos de testemunhas",
                    "Procure atendimento psicológico para lidar com o trauma"
                ]
            },
            "estupro": {
                "definicao": "Constranger alguém por meio de violência ou ameaças a atos sexuais, ou envolver-se sexualmente com quem não pode consentir (alcoolizada/dormindo).",
                "gravidade": "gravissima",
                "palavras_chave": ["constranger", "violência", "ameaças", "sem consentimento"],
                "canais_denuncia": ["Polícia", "Delegacia da Mulher", "Ouvidoria"],
                "recomendacoes": [
                    "Busque atendimento médico imediato em hospital de referência",
                    "Não tome banho nem troque de roupa para preservação de provas físicas",
                    "Acione a Delegacia Especializada de Atendimento à Mulher ou equivalente",
                    "Solicite o kit de profilaxia para ISTs, HIV e contracepção de emergência",
                    "Procure apoio psicológico especializado em trauma sexual",
                    "Solicite medidas protetivas de urgência contra o agressor",
                    "Busque acompanhamento jurídico para os procedimentos legais subsequentes",
                    "A denúncia à polícia é fundamental por se tratar de crime grave"
                ]
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
    },

    "gordofobia": {
        "definicao": "Discriminação, preconceito ou estigmatização baseada no peso corporal ou aparência física relacionada ao peso da pessoa.",
        "gravidade": "media_alta",
        "palavras_chave": ["gordo", "peso", "corpo grande", "sobrepeso", "obeso", "obesidade", "gordura"],
        "canais_denuncia": ["Ouvidoria", "Comissão de Ética"],
        "recomendacoes": [
            "Documente situações de discriminação relacionadas ao peso",
            "Registre denúncia junto à Ouvidoria e Comissão de Ética da instituição",
            "Solicite adequações necessárias para acessibilidade quando aplicável",
            "Busque apoio em grupos de aceitação corporal e movimentos anti-gordofobia",
            "Procure acompanhamento psicológico para lidar com impactos na autoestima",
            "Considere reportar casos graves ao Ministério Público (discriminação)",
            "Conheça seus direitos relacionados à não-discriminação por características físicas"
        ],
        "subtipos": {
            "discriminacao_direta": {
                "definicao": "Insultos, piadas e comentários depreciativos explícitos relacionados ao peso da pessoa.",
                "palavras_chave": ["piada sobre peso", "insulto", "comentários sobre aparência"],
                "comportamentos": ["fazer piadas sobre peso", "insultar baseado no tamanho do corpo"]
            },
            "discriminacao_estrutural": {
                "definicao": "Exclusão sistemática e barreiras físicas ou sociais baseadas em peso e tamanho corporal.",
                "palavras_chave": ["exclusão", "barreira", "acessibilidade", "mobilidade limitada"],
                "comportamentos": ["negar acesso", "excluir de atividades", "não fornecer adaptações"]
            }
        }
    },

    "capacitismo": {
        "definicao": "Discriminação e preconceito contra pessoas com deficiência, incluindo barreiras atitudinais, físicas e institucionais que limitam sua participação plena na sociedade.",
        "gravidade": "media_alta",
        "palavras_chave": ["deficiência", "acessibilidade", "capacitismo", "inclusão", "adaptação"],
        "canais_denuncia": ["Ouvidoria", "Núcleo de Acessibilidade", "Comissão de Ética"],
        "recomendacoes": [
            "Documente detalhadamente barreiras encontradas com descrições precisas e fotos",
            "Solicite formalmente e por escrito as adaptações necessárias à acessibilidade",
            "Reporte situações discriminatórias à Ouvidoria, Núcleo de Acessibilidade e Comissão de Ética",
            "Conheça a legislação específica sobre direitos das pessoas com deficiência",
            "Busque orientação do Núcleo de Acessibilidade da instituição",
            "Conecte-se com organizações e coletivos de pessoas com deficiência",
            "Considere denúncia ao Ministério Público em casos de negação sistemática de direitos básicos",
            "Explore a possibilidade de tecnologias assistivas adequadas à sua necessidade"
        ],
        "subtipos": {
            "barreiras_fisicas": {
                "definicao": "Obstáculos estruturais ou arquitetônicos que impedem o acesso e a mobilidade de pessoas com deficiência.",
                "palavras_chave": ["barreira arquitetônica", "falta de rampa", "acesso físico"],
                "comportamentos": ["não fornecer adaptações razoáveis", "negligenciar acessibilidade"]
            },
            "barreiras_atitudinais": {
                "definicao": "Comportamentos discriminatórios, estereótipos e preconceitos que diminuem as capacidades da pessoa com deficiência.",
                "palavras_chave": ["pena", "incapaz", "superproteção", "infantilização"],
                "comportamentos": ["tratar com infantilização", "tomar decisões pela pessoa"]
            }
        }
    },

    "violencia_digital": {
        "definicao": "Agressões, assédio, intimidação ou exposição não consentida em ambiente digital ou através de tecnologias de comunicação.",
        "gravidade": "alta",
        "palavras_chave": ["cyberbullying", "exposição online", "ameaças virtuais", "mensagens ofensivas"],
        "canais_denuncia": ["Ouvidoria", "Polícia", "Plataformas Digitais"],
        "recomendacoes": [
            "Preserve todas as evidências digitais (capturas de tela, mensagens, e-mails)",
            "Bloqueie o contato com o agressor em todas as plataformas",
            "Reporte o conteúdo abusivo às plataformas onde ele foi publicado",
            "Ajuste suas configurações de privacidade em todas as redes sociais",
            "Documente todas as ocorrências com datas e descrições precisas"
        ],
        "subtipos": {
            "cyberbullying": {
                "definicao": "Intimidação sistemática em ambiente digital, usando textos, fotos ou vídeos para humilhar ou ameaçar.",
                "gravidade": "alta",
                "palavras_chave": ["intimidar online", "humilhação digital", "perseguição virtual"],
                "canais_denuncia": ["Ouvidoria", "Plataformas Digitais"],
                "recomendacoes": [
                    "Preserve todas as evidências com capturas de tela datadas e arquivamento de mensagens",
                    "Bloqueie e reporte o agressor nas plataformas utilizadas",
                    "Ajuste configurações de privacidade em todas as redes sociais",
                    "Reporte o comportamento à Ouvidoria e instâncias disciplinares da instituição",
                    "Busque apoio psicológico para lidar com os impactos emocionais",
                    "Em casos graves, acione a Delegacia de Crimes Cibernéticos"
                ]
            },
            "exposicao_nao_consentida": {
                "definicao": "Compartilhamento de imagens, vídeos ou informações privadas sem consentimento.",
                "gravidade": "gravissima",
                "palavras_chave": ["revenge porn", "vazamento", "compartilhar fotos íntimas"],
                "canais_denuncia": ["Polícia", "Delegacia de Crimes Digitais"],
                "recomendacoes": [
                    "Preserve todas as evidências com urgência (capturas de tela, URLs, mensagens)",
                    "Contate as plataformas imediatamente para remoção do conteúdo",
                    "Registre Boletim de Ocorrência em Delegacia de Crimes Digitais (é crime!)",
                    "Busque orientação jurídica especializada para medidas legais contra o agressor",
                    "Considere ajuda técnica para identificar a extensão da exposição online",
                    "Procure acompanhamento psicológico para o trauma relacionado à violação",
                    "Denúncia à polícia é essencial nestes casos"
                ]
            }
        }
    },

    "discriminacao_religiosa": {
        "definicao": "Preconceito, exclusão ou tratamento desigual baseado na crença, religião ou prática espiritual de uma pessoa.",
        "gravidade": "media_alta",
        "palavras_chave": ["intolerância religiosa", "preconceito religioso", "crença", "fé", "religião"],
        "canais_denuncia": ["Ouvidoria", "Comissão de Ética"],
        "recomendacoes": [
            "Documente detalhadamente os incidentes de intolerância religiosa",
            "Busque apoio na comunidade religiosa e em grupos de direitos humanos",
            "Formalize denúncia junto à Ouvidoria e Comissão de Ética institucional",
            "Solicite espaços e momentos para práticas religiosas quando necessário",
            "Informe-se sobre as políticas institucionais relativas à liberdade religiosa",
            "Denuncie à polícia casos de violência ou impedimento do culto religioso, pois constituem crime",
            "Promova diálogos interreligiosos para combater o preconceito"
        ],
        "subtipos": {
            "ofensa_direta": {
                "definicao": "Insultos, desrespeito ou ridicularização explícita de símbolos, práticas ou crenças religiosas.",
                "palavras_chave": ["insulto religioso", "zombar de religião", "ridicularizar crença"],
                "comportamentos": ["fazer piadas com símbolos religiosos", "desrespeitar práticas"]
            },
            "discriminacao_institucional": {
                "definicao": "Políticas ou práticas que dificultam ou impedem a observância de preceitos religiosos.",
                "palavras_chave": ["impedimento de prática", "negação de direito religioso"],
                "comportamentos": ["negar dias santos", "impedir uso de vestimentas religiosas"]
            }
        }
    },

    "xenofobia": {
        "definicao": "Preconceito, discriminação ou hostilidade contra pessoas de outros países, regiões ou culturas, consideradas estrangeiras.",
        "gravidade": "media_alta",
        "palavras_chave": ["estrangeiro", "imigrante", "nacionalidade", "origem", "sotaque", "regionalismo"],
        "canais_denuncia": ["Ouvidoria", "Comissão de Ética", "Núcleo de Direitos Humanos"],
        "recomendacoes": [
            "Mantenha um registro detalhado de comentários e ações discriminatórias",
            "Reporte incidentes ao setor de relações internacionais ou núcleo de diversidade da instituição",
            "Forme redes de apoio com outros estudantes internacionais ou migrantes",
            "Denuncie formalmente à Ouvidoria e Comissão de Ética",
            "Participe de atividades culturais que valorizem a diversidade regional/internacional",
            "Busque apoio psicológico especializado em questões interculturais",
            "Em casos graves, denuncie à polícia (injúria por procedência nacional é crime)"
        ],
        "subtipos": {
            "discriminacao_regional": {
                "definicao": "Preconceito contra pessoas de diferentes regiões do país, incluindo sotaque, costumes e cultura.",
                "palavras_chave": ["preconceito regional", "sotaque", "nordestino", "nortista", "caipira"],
                "comportamentos": ["imitar sotaque de forma pejorativa", "fazer piadas regionais"]
            },
            "xenofobia_internacional": {
                "definicao": "Discriminação direcionada especificamente a pessoas de outros países.",
                "palavras_chave": ["estrangeiro", "imigrante", "refugiado", "país de origem"],
                "comportamentos": ["negar serviços", "hostilizar por nacionalidade", "comentários xenófobos"]
            }
        }
    },
    "discriminacao_racial": {
        "definicao": "Discriminação, preconceito ou estigmatização baseada em raça, cor, etnia ou características fenotípicas.",
        "gravidade": "alta",
        "palavras_chave": ["racismo", "insulto racial", "discriminação racial", "preconceito racial"],
        "canais_denuncia": ["Ouvidoria", "Comissão de Ética", "Polícia"],
        "recomendacoes": [
            "Registre detalhadamente todos os episódios com data, hora, local e presentes",
            "Identifique possíveis testemunhas que possam corroborar seu relato",
            "Preserve evidências como mensagens, e-mails ou registros audiovisuais",
            "Acione imediatamente a Ouvidoria e Comissão de Ética da instituição",
            "Busque apoio em núcleos de estudos afro-brasileiros ou coletivos antirracistas",
            "Formalize Boletim de Ocorrência na polícia (racismo é crime inafiançável)",
            "Procure acompanhamento psicológico especializado em traumas raciais",
            "Considere acionar o Ministério Público em casos de racismo institucional"
        ],
        "subtipos": {
            "ofensa_direta": {
                "definicao": "Insultos, piadas e comentários depreciativos explícitos relacionados à raça/etnia.",
                "palavras_chave": ["insulto racial", "xingamento", "ofensa"],
                "comportamentos": ["usar termos pejorativos", "fazer comparações ofensivas"]
            },
            "discriminacao_estrutural": {
                "definicao": "Exclusão sistemática e barreiras baseadas em raça/etnia.",
                "palavras_chave": ["exclusão", "barreira", "tratamento diferenciado"],
                "comportamentos": ["negar acesso", "excluir de atividades", "tratamento desfavorável"]
            }
        }
    }
}



SEVERITY_RANKING = {
    "violencia_sexual": {
        "estupro": 10,
        "importunacao_sexual": 8,
        "assedio_sexual": 7,
        "outras_condutas_conotacao_sexual": 5
    },
    "perseguicao": 7,
    "abuso_psicologico": 6,
    "assedio_moral_genero": 6,
    "discriminacao_genero": {
        "discriminacao_flagrante": 5,
        "discriminacao_sutil": 4
    },
    "microagressoes": {
        "interrupcoes_constantes": 2,
        "questionar_julgamento": 2,
        "comentarios_saude_mental": 3,
        "estereotipos": 2
    },
    "gordofobia": {
        "discriminacao_direta": 4,
        "discriminacao_estrutural": 5
    },
    "capacitismo": {
        "barreiras_fisicas": 5,
        "barreiras_atitudinais": 4
    },
    "violencia_digital": {
        "cyberbullying": 5,
        "exposicao_nao_consentida": 8
    },
    "discriminacao_religiosa": {
        "ofensa_direta": 4,
        "discriminacao_institucional": 5
    },
    "xenofobia": {
        "discriminacao_regional": 4,
        "xenofobia_internacional": 5
    },
    "discriminacao_racial": {
        "ofensa_direta": 7,
        "discriminacao_estrutural": 8
    }
}

# Definição da gravidade e procedimentos gerais
SEVERITY_LEVEL = {
    "baixa": "Comportamento inadequado que requer atenção e orientação.",
    "baixa_cumulativa": "Comportamentos que individualmente são de baixa gravidade, mas podem causar danos significativos quando repetidos.",
    "media_baixa": "Violação que requer intervenção e possível advertência.",
    "media": "Violação que requer intervenção institucional e possíveis medidas disciplinares.",
    "media_alta": "Violação séria que pode resultar em medidas disciplinares mais severas.",
    "alta": "Violação grave que requer ações imediatas de proteção.",
    "gravissima": "Violação extremamente grave que constitui crime passível de expulsão."
}

# Canais de denúncia e suas descrições
REPORT_CONTACT = {
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

def get_severity(vtype, subtype=None):
    """Obtém o nível de gravidade para um tipo/subtipo de violência."""
    if vtype in SEVERITY_RANKING:
        if isinstance(SEVERITY_RANKING[vtype], dict) and subtype:
            return SEVERITY_RANKING[vtype].get(subtype, 0)
        elif not isinstance(SEVERITY_RANKING[vtype], dict):
            return SEVERITY_RANKING[vtype]
    return 0