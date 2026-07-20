from models.severity_model import predict_v1, predict_v2
from rollout.rollout_manager import rollout_manager


def predict_with_model(model_version, text):
    if model_version == "v2":
        return predict_v2(text)

    return predict_v1(text)


def predict_with_rollout(text):
    decision_model, rollout_mode = rollout_manager.choose_model_for_request()

    decision_prediction = predict_with_model(decision_model, text)
    shadow_model = rollout_manager.get_shadow_model(decision_model)

    response = {
        "severity": decision_prediction["severity"],
        "confidence": decision_prediction["confidence"],
        "model_version": decision_prediction["model_version"],
        "rollout_mode": rollout_mode,
        "used_for_decision": True
    }

    if shadow_model:
        shadow_prediction = predict_with_model(shadow_model, text)
        response["shadow_prediction"] = {
            "severity": shadow_prediction["severity"],
            "confidence": shadow_prediction["confidence"],
            "model_version": shadow_prediction["model_version"],
            "used_for_decision": False
        }

    return response