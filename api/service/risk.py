import json, os

def user_risk(user_input_country):
    risk_data_score = {}
    current_dir = os.path.dirname(__file__) 
    risk_data_score["score"] = 0
    risk_data_score["alert"] = []
    risk_data = os.path.join(current_dir, "..", "data", "country_code_data_three.json")
    with open(risk_data, "r", encoding="utf-8") as f:
        risk_data = json.load(f)
    for i in range(len(risk_data)):
        if risk_data[i]["ntnNm"] == user_input_country:
            if risk_data[i]["alertNm"] == "Y": #자연재해/기상 경고
                risk_data_score["score"] += 5
                risk_data_score["alert"].append("자연재해 경고")
            if risk_data[i]["alertCt"] == "Y": #치안 위험 경고
                risk_data_score["score"] += 7
                risk_data_score["alert"].append("치안 위험 경고")
            if risk_data[i]["alertRc"] == "Y": #전염병 위험 경고
                risk_data_score["score"] += 5
                risk_data_score["alert"].append("전염병 경고")
            if risk_data[i]["alertBn"] == "Y": #테러/사회 불안 경고
                risk_data_score["score"] += 10
                risk_data_score["alert"].append("테러 경고")
            if risk_data[i]["alertAl"] == "Y": #기타 경고
                risk_data_score["score"] += 3  
                risk_data_score["alert"].append("사회경고")                 
    return risk_data_score



