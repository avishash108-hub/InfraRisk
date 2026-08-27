from flask import Flask, jsonify, request, session
import psycopg
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os


import os
def get_db():
    con = psycopg.connect(
        dbname = 'DB_NAME',
        host = "DB_HOST",
        password = "DB_PASSWORD",
        user = "DB_USER",
        port  = 5432
    )
    return con

ph = PasswordHasher(time_cost = 3, memory_cost = 65536, parallelism = 4)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
@app.route('/')
def home():
    return "flask working", 200


@app.route('/login', methods = ['POST'])
#request = {
    # 'gov_id' : '...',
    # 'pwd' : ...
#}'''
def login():
  data = request.get_json()
  gov_id = data.get("gov_id")
  password = data.get("pwd")
  if not gov_id:
      return jsonify({"error" : "Please enter your Government ID"}), 400
  if not password:
      return jsonify({"error" : "Please enter the password"}), 400
  con = get_db()
  cur = con.cursor()
  cur.execute('''
  select
  gov_id, 
  pwd_hash 
  from users 
  where gov_id = %s''',
  (gov_id,)
  )
  result = cur.fetchone()
  if result is None:
    return jsonify({"error": "Invalid Government ID or password"}), 401      
  
  pwd_hash = result[1]
  try:
    ph.verify(pwd_hash, password)
  except VerifyMismatchError:
      return jsonify({"error": "Invalid Government ID or password"}), 401


  cur.execute("""
    SELECT gov_role
    FROM users
    WHERE gov_id = %s
  """,
 (gov_id,)
 )

 
  result = cur.fetchone()

  if result is None:
    return jsonify({"error": "User role not found"}), 404

  role = result[0]

  session["gov_id"] = gov_id
  session["role"] = role
  print("SESSION AFTER LOGIN:", dict(session))
  print("SESSION IN PROTECTED ROUTE:", dict(session))

  return jsonify({
    "message": "Login successful",
    "role": role
}), 200




#dashboard for municipal officer


def mun_officer_dash():
   '''material_lookup = {
      "METALLIC" : 80,
      "CI" : 60
   }'''
   total_drainage_health = 0
   con = get_db()
   cur = con.cursor()
   cur.execute('''
     select material,
     installation_year,
     leak_count,
     expected_life
     from pipelines

   ''')
   drainage_result = cur.fetchall() #returns all 100 rows

   cur.execute('''
   select max(leak_count), min(leak_count) 
   from pipelines
   ''')
   max_lc, min_lc = cur.fetchone() 

   for drainage in drainage_result:
      material = drainage[0]
      installation_year = drainage[1]
      leak_count = drainage[2]
      expected_age = drainage[3]

      #material health(score is arbitrary based on strength of the material)
      if material == "METALLIC":
         material_health = 80
      elif material == "CI":
         material_health = 60

      #age_risk
      age = 2026 - installation_year
      age_risk = min((age / expected_age) * 100 , 100) #normalized age_risk score
      age_health = 100 - age_risk

      #leakage
      if max_lc == min_lc:
         leakage_health = 100
      else:
         leakage_risk = (
            (
               (leak_count - min_lc)
               / (max_lc - min_lc)
            ) * 100
         )
         leakage_health = 100 - leakage_risk

      drainage_health = (
         material_health +
         age_health +
         leakage_health
      ) / 3

      total_drainage_health += drainage_health

   cur.close()
   con.close()

   final_drainage_health = total_drainage_health / len(drainage_result)


   #ROAD_HEALTH
   con = get_db()
   cur = con.cursor()
   cur.execute("""
    SELECT
        installation_year,
        expected_life_years,
        condition_score,
        accidents_last_3_years,
        environmental_exposure
    FROM roads
   """)

   road_results = cur.fetchall()
   cur.close()
   con.close()

   max_accidents = max(row[3] for row in road_results)
   min_accidents = min(row[3] for row in road_results)

   max_env = max(row[4] for row in road_results)
   min_env = min(row[4] for row in road_results)

   total_road_health = 0

   for road in road_results:
      installation_year = road[0]
      expected_life = road[1]
      condition_score = road[2]
      accidents = road[3]
      environment = road[4]

      #age_risk
      age = 2026 - installation_year
      age_risk = min((age / expected_life) * 100, 100)
      age_health = 100 - age_risk

      #accident_risk
      if max_accidents == min_accidents:
         accident_health = 100
      else:
         accident_risk = (
            (accidents - min_accidents)
            / (max_accidents - min_accidents)
         ) * 100

         accident_health = 100 - accident_risk

      if max_env == min_env:
         environment_health = 100
      else:
         environment_risk = (
            (environment - min_env)
            / (max_env - min_env)
         ) * 100

         environment_health = 100 - environment_risk

      condition_health = condition_score

      #Individual road health
      road_health = (
         age_health +
         accident_health +
         environment_health +
         condition_health
      ) / 4

      total_road_health += road_health

   final_road_health = total_road_health / len(road_results)


   #BRIDE HEALTH
   con = get_db()
   cur = con.cursor()
   cur.execute("""
    SELECT
        bridge_installation_year,
        expected_life_years,
        condition_score,
        environmental_exposure,
        accidents_last_3_years
    FROM bridges
   """)

   bridges = cur.fetchall()
   cur.close()
   con.close()

   total_bridge_health = 0

   #Find min/max for normalization
   max_accidents = max(row[4] for row in bridges)
   min_accidents = min(row[4] for row in bridges)

   max_environment = max(row[3] for row in bridges)
   min_environment = min(row[3] for row in bridges)

   for bridge in bridges:

      installation_year = bridge[0]
      expected_life = bridge[1]
      condition_score = bridge[2]
      environment = bridge[3]
      accidents = bridge[4]

      #AGE
      age = 2026 - installation_year

      age_risk = min(
         (age / expected_life) * 100,
         100
      )

      age_health = 100 - age_risk

      #ACCIDENT
      if max_accidents == min_accidents:
         accident_health = 100
      else:
         accident_risk = (
            (accidents - min_accidents)
            / (max_accidents - min_accidents)
         ) * 100

         accident_health = 100 - accident_risk

      #ENVIRONMENT
      if max_environment == min_environment:
         environment_health = 100
      else:
         environment_risk = (
            (environment - min_environment)
            / (max_environment - min_environment)
         ) * 100

         environment_health = 100 - environment_risk

      #CONDITION
      condition_health = condition_score

      #INDIVIDUAL BRIDGE HEALTH
      bridge_health = (
         age_health +
         accident_health +
         environment_health +
         condition_health
      ) / 4

      total_bridge_health += bridge_health


   #BRIDGE NETWORK HEALTH
   final_bridge_health = (
      total_bridge_health / len(bridges)
   )

   #OVERALL HEALTH
   overall_health = (
      final_drainage_health +
      final_road_health +
      final_bridge_health
   ) / 3

   return jsonify({
      "drainage_health": round(final_drainage_health, 2),
      "road_health": round(final_road_health, 2),
      "bridge_health": round(final_bridge_health, 2),
      "overall_health": round(overall_health, 2)
   })

#def field_inspector_dash():

@app.route('/dashboard', methods = ['GET'])

def dashboard():
   role = session.get("role")

   if role == "municipal officer":
        return mun_officer_dash()

   
   #feature under development
   elif role == "field inspector":
        return field_inspector_dash()

   else:
        return jsonify({"error": "Unauthorized"}), 401



@app.route('/assets', methods=['GET'])
def assets():

    role = session.get("role")

    if not role:
        return jsonify({"error": "Unauthorized"}), 401

    con = get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT asset_id, asset_type, condition_score, risk_score
        FROM assets
    """)

    assets = cur.fetchall()

    total_assets = len(assets)
    high_risk = 0
    critical = 0

    asset_list = []

    for asset in assets:

        asset_id = asset[0]
        asset_type = asset[1]
        condition_score = asset[2]
        risk_score = asset[3]

        if risk_score >= 85:
            status = "Critical"
            critical += 1
        elif risk_score >= 65:
            status = "High"
            high_risk += 1
        elif risk_score >= 45:
            status = "Moderate"
        else:
            status = "Low"

        asset_list.append({
            "asset_id": asset_id,
            "asset_type": asset_type,
            "condition_score": condition_score,
            "risk_score": round(risk_score, 2),
            "status": status
        })

    return jsonify({
        "total_assets": total_assets,
        "high_risk_assets": high_risk,
        "critical_assets": critical,
        "assets": asset_list
    }), 200

if __name__ == '__main__':
    app.run(debug = True)
