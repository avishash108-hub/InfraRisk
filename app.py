#backend is yet to be merged with the frontend, this is raw code in process. More endpoints to be added. This will be deployed on Render.


from flask import Flask, jsonify, request
import pandas as pd

from risk_engine import calculate_risks


app = Flask(__name__)

assets = pd.read_csv("assets.csv")


def get_ranges():
    traffic_min = assets["traffic"].min()
    traffic_max = assets["traffic"].max()

    accident_min = assets["accidents"].min()
    accident_max = assets["accidents"].max()

    return (
        traffic_min,
        traffic_max,
        accident_min,
        accident_max
    )


def get_asset_risk(asset):
    (
        traffic_min,
        traffic_max,
        accident_min,
        accident_max
    ) = get_ranges()

    return calculate_risks(
        asset,
        traffic_min,
        traffic_max,
        accident_min,
        accident_max
    )


@app.route("/assets", methods=["GET"])
def get_assets():

    result = []

    for _, asset in assets.iterrows():

        risk = get_asset_risk(asset)

        result.append({
            "asset_id": int(asset["asset_id"]),
            "asset_type": asset["asset_type"],
            "condition": float(asset["condition"]),
            "age": float(asset["age"]),
            "risk_score": risk["risk_score"],
            "classification": risk["classification"],
            "repair_cost": float(asset["repair_cost"])
        })

    return jsonify(result)




@app.route("/dashboard", methods=["GET"])
def dashboard():

    risk_scores = []
    classifications = []

    condition_scores = []

    for _, asset in assets.iterrows():

        risk = get_asset_risk(asset)

        risk_scores.append(risk["risk_score"])
        classifications.append(risk["classification"])
        condition_scores.append(float(asset["condition"]))

    total = len(assets)

    return jsonify({
        "total_assets": total,
        "average_risk": round(sum(risk_scores) / total, 2),
        "network_condition_index":
            round(sum(condition_scores) / total, 2),

        "critical": classifications.count("Critical"),
        "high": classifications.count("High"),
        "moderate": classifications.count("Moderate"),
        "low": classifications.count("Low")
    })


@app.route("/assets/<int:asset_id>/risk", methods=["GET"])
def asset_risk(asset_id):

    matching = assets[assets["asset_id"] == asset_id]

    if matching.empty:
        return jsonify({"error": "Asset not found"}), 404

    asset = matching.iloc[0]

    risk = get_asset_risk(asset)

    return jsonify({
        "asset_id": asset_id,
        "risk": risk
    })


if name == "__main__":
  app.run(debug = True)
