"""
Fábrica para criação de tipos de violência.
"""
from typing import Dict
from ..models.violence_type import ViolenceType, ViolenceSubtype, Severity, ReportChannel
from ..models.criteria import CriterionWeights


class ViolenceTypeFactory:
    """Fábrica para criar tipos de violência de forma consistente."""
    
    @staticmethod
    def create_microagressoes() -> ViolenceType:
        """Cria o tipo de violência: microagressões."""
        main_type = ViolenceType(
            name="microagressoes",
            definition="Comentários e comportamentos sutis, muitas vezes inconscientes, que desrespeitam, desvalorizam ou diminuem a dignidade de uma pessoa com base em sua identidade de grupo.",
            severity=Severity.BAIXA_CUMULATIVA,
            keywords=["interromper", "cortar fala", "silenciar", "duvidar", "contestar", "histérico", "emocional"],
            common_targets=["condições financeiras diferentes", "raça", "gênero", "deficiência física", "deficiência mental"],
            report_channels=["Ouvidoria", "Coordenacao_Curso"],
            recommendations=[
                "Documente cada incidente com data, hora, local e detalhes sobre o que foi dito/feito",
                "Comunique claramente seus limites: 'Esse comentário me faz sentir desconfortável'",
                "Busque apoio em coletivos identitários ou grupos de afinidade na instituição",
                "Converse com colegas que possam ter testemunhado para validar sua experiência",
                "Reporte padrões recorrentes à Ouvidoria institucional ou à Coordenação",
                "Considere abordar o assunto em reuniões departamentais se o problema for sistemático",
                "Preserve sua saúde mental buscando apoio psicológico se necessário"
            ],
            severity_score=2
        )
        
        # Subtipos
        main_type.add_subtype(ViolenceSubtype(
            name="interrupcoes_constantes",
            definition="Interromper alguém enquanto fala, especialmente quando é um padrão recorrente direcionado a pessoas de grupos marginalizados.",
            keywords=["interromper", "cortar fala", "silenciar", "não deixar falar"],
            behaviors=["interrupções repetidas", "desvalorização da fala"],
            severity_score=2
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="questionar_julgamento",
            definition="Sempre questionar julgamentos mesmo que válidos.",
            keywords=["duvidar", "contestar", "questionar capacidade"],
            behaviors=["duvidar constantemente", "contestar decisões válidas"],
            severity_score=2
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="comentarios_saude_mental",
            definition="Comentários sobre estado de saúde mental ou emocional utilizados para diminuir ou deixar a pessoa desconfortável.",
            keywords=["histérico", "emocional", "sensível", "exagerado"],
            behaviors=["minimizar reclamações", "patologizar reações normais"],
            severity_score=3
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="estereotipos",
            definition="Insultos, comentários e piadas sobre estereótipos que a pessoa se encontra.",
            keywords=["piada", "brincadeira", "zoação", "estereótipo"],
            behaviors=["fazer piadas estereotipadas", "comentários depreciativos"],
            severity_score=2
        ))
        
        return main_type

    @staticmethod
    def create_perseguicao() -> ViolenceType:
        """Cria o tipo de violência: perseguição."""
        return ViolenceType(
            name="perseguicao",
            definition="Perseguir alguém, repetidamente e por qualquer meio, ameaçando sua integridade física ou psicológica, restringindo sua capacidade de ir e vir ou invadindo sua liberdade ou privacidade.",
            severity=Severity.ALTA,
            keywords=["perseguir", "vigiar", "seguir", "stalking", "ameaçar"],
            report_channels=["Ouvidoria", "Seguranca_Campus", "Policia"],
            recommendations=[
                "Notifique imediatamente autoridades competentes (Segurança do Campus e, em casos graves, a Polícia)",
                "Nunca confronte o perseguidor diretamente ou sozinho(a)",
                "Registre detalhadamente cada ocorrência (datas, horários, locais e descrições)",
                "Preserve todas as evidências: mensagens, e-mails, presentes indesejados",
                "Modifique suas rotinas e trajetos para dificultar a previsibilidade",
                "Informe pessoas próximas sobre a situação para ampliar sua rede de proteção",
                "Solicite medidas protetivas através dos canais institucionais e/ou judiciais",
                "Reporte à Polícia se houver ameaças explícitas ou comportamento intimidador persistente"
            ],
            severity_score=7
        )

    @staticmethod
    def create_violencia_sexual() -> ViolenceType:
        """Cria o tipo de violência: violência sexual."""
        main_type = ViolenceType(
            name="violencia_sexual",
            definition="Categoria que engloba diferentes condutas de natureza sexual não consentidas.",
            severity=Severity.ALTA,
            report_channels=["Policia", "Ouvidoria", "Delegacia_Mulher"],
            recommendations=[
                "Busque um ambiente seguro imediatamente",
                "Preserve todas as evidências possíveis",
                "Reporte o incidente às autoridades competentes"
            ],
            severity_score=8
        )
        
        # Subtipos
        main_type.add_subtype(ViolenceSubtype(
            name="assedio_sexual",
            definition="Condutas de natureza sexual, não consentidas, que causam constrangimento e prejuízo à dignidade, intimidade, privacidade, honra e liberdade sexual.",
            keywords=["natureza sexual", "não consentida", "constrangimento"],
            report_channels=["Ouvidoria", "Comissao_Etica", "Policia"],
            recommendations=[
                "Registre detalhadamente cada ocorrência com data, hora e descrição precisa",
                "Reporte imediatamente à Ouvidoria e à Comissão de Ética",
                "Busque apoio em serviços de atendimento psicológico institucional",
                "Evite situações de isolamento com o assediador",
                "Considere denúncia formal aos órgãos competentes da instituição",
                "Busque orientação jurídica para conhecer todas as possibilidades de ação"
            ],
            severity_score=7
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="importunacao_sexual",
            definition="Praticar ato obsceno contra alguém sem consentimento, para satisfazer impulso sexual ou humilhar/intimidar.",
            keywords=["ato obsceno", "sem consentimento", "impulso sexual"],
            report_channels=["Ouvidoria", "Policia"],
            recommendations=[
                "Notifique imediatamente as autoridades de segurança presentes",
                "Busque ajuda de pessoas próximas para intervir e testemunhar",
                "Registre Boletim de Ocorrência em delegacia especializada (crime previsto em lei)",
                "Solicite medidas protetivas contra o agressor",
                "Preserve evidências como gravações, mensagens ou relatos de testemunhas",
                "Procure atendimento psicológico para lidar com o trauma"
            ],
            severity_score=8
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="estupro",
            definition="Constranger alguém por meio de violência ou ameaças a atos sexuais, ou envolver-se sexualmente com quem não pode consentir (alcoolizada/dormindo).",
            keywords=["constranger", "violência", "ameaças", "sem consentimento"],
            report_channels=["Policia", "Delegacia_Mulher", "Ouvidoria"],
            recommendations=[
                "Busque atendimento médico imediato em hospital de referência",
                "Não tome banho nem troque de roupa para preservação de provas físicas",
                "Acione a Delegacia Especializada de Atendimento à Mulher ou equivalente",
                "Solicite o kit de profilaxia para ISTs, HIV e contracepção de emergência",
                "Procure apoio psicológico especializado em trauma sexual",
                "Solicite medidas protetivas de urgência contra o agressor",
                "Busque acompanhamento jurídico para os procedimentos legais subsequentes",
                "A denúncia à polícia é fundamental por se tratar de crime grave"
            ],
            severity_score=10
        ))
        
        return main_type

    @staticmethod
    def create_discriminacao_genero() -> ViolenceType:
        """Cria o tipo de violência: discriminação de gênero."""
        main_type = ViolenceType(
            name="discriminacao_genero",
            definition="Inclui qualquer exclusão, restrição ou preferência com base no sexo, gênero, orientação sexual ou identidade e expressão, ou qualquer outra limitação que interfira no reconhecimento ou exercício de direitos fundamentais.",
            severity=Severity.MEDIA_ALTA,
            keywords=["exclusão", "restrição", "preferência", "sexo", "gênero"],
            report_channels=["Ouvidoria", "Comissao_Etica"],
            recommendations=[
                "Registre situações discriminatórias com detalhes específicos e nomes de testemunhas",
                "Consulte o núcleo de diversidade ou comissão de igualdade de gênero da instituição",
                "Formalize denúncia à Ouvidoria e à Comissão de Ética institucional",
                "Busque apoio em coletivos feministas ou LGBTQIA+ para orientação e suporte",
                "Informe-se sobre políticas de gênero vigentes na instituição",
                "Considere acompanhamento psicológico para lidar com os impactos emocionais",
                "Em casos de discriminação flagrante e sistemática, considere denúncia ao Ministério Público"
            ],
            severity_score=5
        )
        
        # Subtipos
        main_type.add_subtype(ViolenceSubtype(
            name="discriminacao_flagrante",
            definition="Acontece de forma aberta através de ações, discursos que defendem práticas discriminatórias.",
            keywords=["explícita", "aberta", "discurso discriminatório"],
            behaviors=["declarações explícitas", "exclusão direta"],
            severity_score=5
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="discriminacao_sutil",
            definition="A mais comum. Acontece através de comportamentos insidiosos e naturalizados cujo propósito discriminatório é mantido oculto.",
            keywords=["sutil", "insidioso", "naturalizado", "oculto"],
            behaviors=["comentários aparentemente inofensivos", "exclusão indireta"],
            severity_score=4
        ))
        
        return main_type
    
    @staticmethod
    def create_abuso_psicologico() -> ViolenceType:
        """Cria o tipo de violência: abuso psicológico."""
        return ViolenceType(
            name="abuso_psicologico",
            definition="Causar danos emocionais que perturbam o desenvolvimento da pessoa ou visam degradar/controlar suas ações por meio de ameaças, constrangimento, humilhação, isolamento, chantagem ou ridicularização.",
            severity=Severity.ALTA,
            keywords=["danos emocionais", "controlar", "ameaças", "constrangimento", "humilhação"],
            report_channels=["Ouvidoria", "Servico_Psicologico", "Comissao_Etica"],
            recommendations=[
                "Registre detalhadamente os episódios, incluindo data, horário, local e testemunhas",
                "Busque apoio psicológico especializado para processar o trauma e desenvolver estratégias",
                "Evite ficar a sós com a pessoa abusadora em qualquer circunstância",
                "Reporte formalmente à Ouvidoria e à Comissão de Ética da instituição",
                "Solicite transferência de setor/turma se compartilhar ambiente com o abusador",
                "Estabeleça limites claros em todas as interações necessárias",
                "Busque apoio em sua rede social (amigos, família, colegas de confiança)",
                "Reporte à Polícia em casos que envolvam ameaças explícitas à segurança"
            ],
            severity_score=6
        )

    @staticmethod
    def create_assedio_moral_genero() -> ViolenceType:
        """Cria o tipo de violência: assédio moral por gênero."""
        return ViolenceType(
            name="assedio_moral_genero",
            definition="Processo contínuo de condutas abusivas que violam a integridade, através da degradação das relações, pressão para tarefas desnecessárias, discriminação, humilhação ou exclusão social.",
            severity=Severity.ALTA,
            keywords=["processo contínuo", "condutas abusivas", "degradação", "humilhação"],
            report_channels=["Ouvidoria", "Comissao_Etica"],
            recommendations=[
                "Documente todas as ocorrências com data, hora, local e descrições precisas",
                "Salve e-mails, mensagens e comunicações que evidenciem o tratamento diferenciado",
                "Procure identificar testemunhas que possam corroborar seu relato",
                "Consulte o setor de recursos humanos ou equivalente sobre políticas de assédio",
                "Acione a Ouvidoria e Comissão de Ética para formalizar denúncia",
                "Busque apoio psicológico para lidar com o estresse e pressão continuados",
                "Considere acompanhamento jurídico especializado em direito trabalhista",
                "Denuncie ao Ministério Público do Trabalho em casos graves e persistentes"
            ],
            severity_score=6
        )

    @staticmethod
    def create_gordofobia() -> ViolenceType:
        """Cria o tipo de violência: gordofobia."""
        main_type = ViolenceType(
            name="gordofobia",
            definition="Discriminação, preconceito ou estigmatização baseada no peso corporal ou aparência física relacionada ao peso da pessoa.",
            severity=Severity.MEDIA_ALTA,
            keywords=["gordo", "peso", "corpo grande", "sobrepeso", "obeso", "obesidade", "gordura"],
            report_channels=["Ouvidoria", "Comissao_Etica"],
            recommendations=[
                "Documente situações de discriminação relacionadas ao peso",
                "Registre denúncia junto à Ouvidoria e Comissão de Ética da instituição",
                "Solicite adequações necessárias para acessibilidade quando aplicável",
                "Busque apoio em grupos de aceitação corporal e movimentos anti-gordofobia",
                "Procure acompanhamento psicológico para lidar com impactos na autoestima",
                "Considere reportar casos graves ao Ministério Público (discriminação)",
                "Conheça seus direitos relacionados à não-discriminação por características físicas"
            ],
            severity_score=4
        )
        
        # Subtipos
        main_type.add_subtype(ViolenceSubtype(
            name="discriminacao_direta",
            definition="Insultos, piadas e comentários depreciativos explícitos relacionados ao peso da pessoa.",
            keywords=["piada sobre peso", "insulto", "comentários sobre aparência"],
            behaviors=["fazer piadas sobre peso", "insultar baseado no tamanho do corpo"],
            severity_score=4
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="discriminacao_estrutural",
            definition="Exclusão sistemática e barreiras físicas ou sociais baseadas em peso e tamanho corporal.",
            keywords=["exclusão", "barreira", "acessibilidade", "mobilidade limitada"],
            behaviors=["negar acesso", "excluir de atividades", "não fornecer adaptações"],
            severity_score=5
        ))
        
        return main_type

    @staticmethod
    def create_capacitismo() -> ViolenceType:
        """Cria o tipo de violência: capacitismo."""
        main_type = ViolenceType(
            name="capacitismo",
            definition="Discriminação e preconceito contra pessoas com deficiência, incluindo barreiras atitudinais, físicas e institucionais que limitam sua participação plena na sociedade.",
            severity=Severity.MEDIA_ALTA,
            keywords=["deficiência", "acessibilidade", "capacitismo", "inclusão", "adaptação"],
            report_channels=["Ouvidoria", "Nucleo_Acessibilidade", "Comissao_Etica"],
            recommendations=[
                "Documente detalhadamente barreiras encontradas com descrições precisas e fotos",
                "Solicite formalmente e por escrito as adaptações necessárias à acessibilidade",
                "Reporte situações discriminatórias à Ouvidoria, Núcleo de Acessibilidade e Comissão de Ética",
                "Conheça a legislação específica sobre direitos das pessoas com deficiência",
                "Busque orientação do Núcleo de Acessibilidade da instituição",
                "Conecte-se com organizações e coletivos de pessoas com deficiência",
                "Considere denúncia ao Ministério Público em casos de negação sistemática de direitos básicos",
                "Explore a possibilidade de tecnologias assistivas adequadas à sua necessidade"
            ],
            severity_score=5
        )
        
        # Subtipos
        main_type.add_subtype(ViolenceSubtype(
            name="barreiras_fisicas",
            definition="Obstáculos estruturais ou arquitetônicos que impedem o acesso e a mobilidade de pessoas com deficiência.",
            keywords=["barreira arquitetônica", "falta de rampa", "acesso físico"],
            behaviors=["não fornecer adaptações razoáveis", "negligenciar acessibilidade"],
            severity_score=5
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="barreiras_atitudinais",
            definition="Comportamentos discriminatórios, estereótipos e preconceitos que diminuem as capacidades da pessoa com deficiência.",
            keywords=["pena", "incapaz", "superproteção", "infantilização"],
            behaviors=["tratar com infantilização", "tomar decisões pela pessoa"],
            severity_score=4
        ))
        
        return main_type

    @staticmethod
    def create_violencia_digital() -> ViolenceType:
        """Cria o tipo de violência: violência digital."""
        main_type = ViolenceType(
            name="violencia_digital",
            definition="Agressões, assédio, intimidação ou exposição não consentida em ambiente digital ou através de tecnologias de comunicação.",
            severity=Severity.ALTA,
            keywords=["cyberbullying", "exposição online", "ameaças virtuais", "mensagens ofensivas"],
            report_channels=["Ouvidoria", "Policia", "Plataformas_Digitais"],
            recommendations=[
                "Preserve todas as evidências digitais (capturas de tela, mensagens, e-mails)",
                "Bloqueie o contato com o agressor em todas as plataformas",
                "Reporte o conteúdo abusivo às plataformas onde ele foi publicado",
                "Ajuste suas configurações de privacidade em todas as redes sociais",
                "Documente todas as ocorrências com datas e descrições precisas"
            ],
            severity_score=6
        )
        
        # Subtipos
        main_type.add_subtype(ViolenceSubtype(
            name="cyberbullying",
            definition="Intimidação sistemática em ambiente digital, usando textos, fotos ou vídeos para humilhar ou ameaçar.",
            keywords=["intimidar online", "humilhação digital", "perseguição virtual"],
            report_channels=["Ouvidoria", "Plataformas_Digitais"],
            recommendations=[
                "Preserve todas as evidências com capturas de tela datadas e arquivamento de mensagens",
                "Bloqueie e reporte o agressor nas plataformas utilizadas",
                "Ajuste configurações de privacidade em todas as redes sociais",
                "Reporte o comportamento à Ouvidoria e instâncias disciplinares da instituição",
                "Busque apoio psicológico para lidar com os impactos emocionais",
                "Em casos graves, acione a Delegacia de Crimes Cibernéticos"
            ],
            severity_score=5
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="exposicao_nao_consentida",
            definition="Compartilhamento de imagens, vídeos ou informações privadas sem consentimento.",
            keywords=["revenge porn", "vazamento", "compartilhar fotos íntimas"],
            report_channels=["Policia", "Delegacia_Crimes_Digitais"],
            recommendations=[
                "Preserve todas as evidências com urgência (capturas de tela, URLs, mensagens)",
                "Contate as plataformas imediatamente para remoção do conteúdo",
                "Registre Boletim de Ocorrência em Delegacia de Crimes Digitais (é crime!)",
                "Busque orientação jurídica especializada para medidas legais contra o agressor",
                "Considere ajuda técnica para identificar a extensão da exposição online",
                "Procure acompanhamento psicológico para o trauma relacionado à violação",
                "Denúncia à polícia é essencial nestes casos"
            ],
            severity_score=8
        ))
        
        return main_type

    @staticmethod
    def create_discriminacao_religiosa() -> ViolenceType:
        """Cria o tipo de violência: discriminação religiosa."""
        main_type = ViolenceType(
            name="discriminacao_religiosa",
            definition="Preconceito, exclusão ou tratamento desigual baseado na crença, religião ou prática espiritual de uma pessoa.",
            severity=Severity.MEDIA_ALTA,
            keywords=["intolerância religiosa", "preconceito religioso", "crença", "fé", "religião"],
            report_channels=["Ouvidoria", "Comissao_Etica"],
            recommendations=[
                "Documente detalhadamente os incidentes de intolerância religiosa",
                "Busque apoio na comunidade religiosa e em grupos de direitos humanos",
                "Formalize denúncia junto à Ouvidoria e Comissão de Ética institucional",
                "Solicite espaços e momentos para práticas religiosas quando necessário",
                "Informe-se sobre as políticas institucionais relativas à liberdade religiosa",
                "Denuncie à polícia casos de violência ou impedimento do culto religioso, pois constituem crime",
                "Promova diálogos interreligiosos para combater o preconceito"
            ],
            severity_score=4
        )
        
        # Subtipos
        main_type.add_subtype(ViolenceSubtype(
            name="ofensa_direta",
            definition="Insultos, desrespeito ou ridicularização explícita de símbolos, práticas ou crenças religiosas.",
            keywords=["insulto religioso", "zombar de religião", "ridicularizar crença"],
            behaviors=["fazer piadas com símbolos religiosos", "desrespeitar práticas"],
            severity_score=4
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="discriminacao_institucional",
            definition="Políticas ou práticas que dificultam ou impedem a observância de preceitos religiosos.",
            keywords=["impedimento de prática", "negação de direito religioso"],
            behaviors=["negar dias santos", "impedir uso de vestimentas religiosas"],
            severity_score=5
        ))
        
        return main_type

    @staticmethod
    def create_xenofobia() -> ViolenceType:
        """Cria o tipo de violência: xenofobia."""
        main_type = ViolenceType(
            name="xenofobia",
            definition="Preconceito, discriminação ou hostilidade contra pessoas de outros países, regiões ou culturas, consideradas estrangeiras.",
            severity=Severity.MEDIA_ALTA,
            keywords=["estrangeiro", "imigrante", "nacionalidade", "origem", "sotaque", "regionalismo"],
            report_channels=["Ouvidoria", "Comissao_Etica", "Nucleo_Direitos_Humanos"],
            recommendations=[
                "Mantenha um registro detalhado de comentários e ações discriminatórias",
                "Reporte incidentes ao setor de relações internacionais ou núcleo de diversidade da instituição",
                "Forme redes de apoio com outros estudantes internacionais ou migrantes",
                "Denuncie formalmente à Ouvidoria e Comissão de Ética",
                "Participe de atividades culturais que valorizem a diversidade regional/internacional",
                "Busque apoio psicológico especializado em questões interculturais",
                "Em casos graves, denuncie à polícia (injúria por procedência nacional é crime)"
            ],
            severity_score=4
        )
        
        # Subtipos
        main_type.add_subtype(ViolenceSubtype(
            name="discriminacao_regional",
            definition="Preconceito contra pessoas de diferentes regiões do país, incluindo sotaque, costumes e cultura.",
            keywords=["preconceito regional", "sotaque", "nordestino", "nortista", "caipira"],
            behaviors=["imitar sotaque de forma pejorativa", "fazer piadas regionais"],
            severity_score=4
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="xenofobia_internacional",
            definition="Discriminação direcionada especificamente a pessoas de outros países.",
            keywords=["estrangeiro", "imigrante", "refugiado", "país de origem"],
            behaviors=["negar serviços", "hostilizar por nacionalidade", "comentários xenófobos"],
            severity_score=5
        ))
        
        return main_type

    @staticmethod
    def create_discriminacao_racial() -> ViolenceType:
        """Cria o tipo de violência: discriminação racial."""
        main_type = ViolenceType(
            name="discriminacao_racial",
            definition="Discriminação, preconceito ou estigmatização baseada em raça, cor, etnia ou características fenotípicas.",
            severity=Severity.ALTA,
            keywords=["racismo", "insulto racial", "discriminação racial", "preconceito racial"],
            report_channels=["Ouvidoria", "Comissao_Etica", "Policia"],
            recommendations=[
                "Registre detalhadamente todos os episódios com data, hora, local e presentes",
                "Identifique possíveis testemunhas que possam corroborar seu relato",
                "Preserve evidências como mensagens, e-mails ou registros audiovisuais",
                "Acione imediatamente a Ouvidoria e Comissão de Ética da instituição",
                "Busque apoio em núcleos de estudos afro-brasileiros ou coletivos antirracistas",
                "Formalize Boletim de Ocorrência na polícia (racismo é crime inafiançável)",
                "Procure acompanhamento psicológico especializado em traumas raciais",
                "Considere acionar o Ministério Público em casos de racismo institucional"
            ],
            severity_score=7
        )
        
        # Subtipos
        main_type.add_subtype(ViolenceSubtype(
            name="ofensa_direta",
            definition="Insultos, piadas e comentários depreciativos explícitos relacionados à raça/etnia.",
            keywords=["insulto racial", "xingamento", "ofensa"],
            behaviors=["usar termos pejorativos", "fazer comparações ofensivas"],
            severity_score=7
        ))
        
        main_type.add_subtype(ViolenceSubtype(
            name="discriminacao_estrutural",
            definition="Exclusão sistemática e barreiras baseadas em raça/etnia.",
            keywords=["exclusão", "barreira", "tratamento diferenciado"],
            behaviors=["negar acesso", "excluir de atividades", "tratamento desfavorável"],
            severity_score=8
        ))
        
        return main_type
