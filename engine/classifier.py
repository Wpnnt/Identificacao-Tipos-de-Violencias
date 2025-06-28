from knowledge_base.violence_types import *
from knowledge_base.confidence_levels import *

def classify_by_mapping(user_input):
    print("\n📥 [DEBUG] Entrada do usuário:", user_input)

    classifications = {}

    for field, answer in user_input.items():
        print(f"\n🔍 Verificando campo '{field}' com valor '{answer}'")

        if field in FORM_OPTION_MAPPING and answer in FORM_OPTION_MAPPING[field]:
            mapping = FORM_OPTION_MAPPING[field][answer]
            print(f"✅ Mapeamento encontrado: {mapping}")
        
            for violence_type, subtype_data in mapping.items():
                if isinstance(subtype_data, dict):
                    for subtype, weight in subtype_data.items():
                        key = (violence_type, subtype)
                        classifications.setdefault(key, 0)
                        classifications[key] += weight
                        print(f"📌 Adicionando peso: ({violence_type}, {subtype}) += {weight}")
                elif isinstance(subtype_data, int):  # Tipo sem subtipo
                    key = (violence_type, None)
                    classifications.setdefault(key, 0)
                    classifications[key] += subtype_data
                    print(f"📌 Adicionando peso: ({violence_type}, None) += {subtype_data}")
        else:
            print(f"⚠️ Nenhum mapeamento para: campo='{field}', valor='{answer}'")

    print("\n📊 Classificações acumuladas:", classifications)

    results = []
    for (vtype, subtype), score in classifications.items():
        threshold = get_threshold(vtype, subtype)
        max_score = get_max_score(vtype, subtype)
        print(f"\n📈 Avaliando ({vtype}, {subtype}) → score={score}, threshold={threshold}, max={max_score}")

        if score >= threshold:
            confidence = min(score / max_score, 1.0) if max_score else 0.0
            label = get_confidence_level_label(confidence)
            print(f"✅ Resultado aceito com confiança: {confidence:.2f} ({label})")

            results.append({
                "violence_type": vtype,
                "subtype": subtype,
                "score": score,
                "threshold": threshold,
                "confidence": confidence,
                "confidence_label": label,
                "definition": _get_definition(vtype, subtype),
                "recommendations": _get_recommendations(vtype, subtype),
                "channels": _get_channels(vtype, subtype)
            })
        else:
            print(f"❌ Ignorado: score abaixo do threshold")

    print("\n✅ Resultados finais:", results)
    return results

# Funções auxiliares para extrair do VIOLENCE_TYPES
def _get_definition(vtype, subtype=None):
    vt_data = VIOLENCE_TYPES.get(vtype, {})
    if subtype:
        return vt_data.get("subtipos", {}).get(subtype, {}).get("definicao", vt_data.get("definicao", ""))
    return vt_data.get("definicao", "")

def _get_recommendations(vtype, subtype=None):
    vt_data = VIOLENCE_TYPES.get(vtype, {})
    return vt_data.get("recomendacoes", [])

def _get_channels(vtype, subtype=None):
    vt_data = VIOLENCE_TYPES.get(vtype, {})
    return vt_data.get("canais_denuncia", [])