#Base URL
http://127.0.0.1:5000
1. Login

POST /login

Authenticates a government user and establishes a session.

Request:

{
    "gov_id": "MCD-MO-001",
    "pwd": "officer001"
}

Success — 200

{
    "message": "Login successful",
    "role": "municipal officer"
}

Missing field — 400

{
    "error": "Please enter your Government ID"
}

Invalid credentials — 401

{
    "error": "Invalid Government ID or password"
}
2. Municipal Officer Dashboard

GET /dashboard

Returns infrastructure health information for the municipal officer.

Success — 200

{
    "drainage_health": 78.42,
    "road_health": 71.35,
    "bridge_health": 82.16,
    "overall_health": 77.31
}

Unauthorized — 401

{
    "error": "Unauthorized"
}
3. Assets

GET /assets

Returns asset statistics and individual asset risk information.

Success — 200

{
    "total_assets": 100,
    "high_risk_assets": 24,
    "critical_assets": 8,
    "assets": [
        {
            "asset_id": "R001",
            "asset_type": "Road",
            "condition_score": 72,
            "risk_score": 68.4,
            "status": "High"
        }
    ]
}
Risk Classification

Risk Score	Status
>= 85	Critical
65–84.99	High
45–64.99	Moderate
< 45	Low
Authentication

The API uses session-based authentication. After successful login, Flask establishes a session containing:

gov_id
role


- Protected routes use this session to determine whether the user is authorized and which dashboard should be displayed.
