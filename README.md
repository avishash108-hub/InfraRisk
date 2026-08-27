# InfraRisk

## Smart Infrastructure Risk Assessment & Repair Prioritization System

InfraRisk is a smart city infrastructure management system designed to help municipal authorities monitor infrastructure health, identify high-risk assets, and prioritize maintenance and repair activities.

The system focuses on roads, bridges, and drainage infrastructure and provides different interfaces for municipal officers and field inspectors.

---

## Problem

Municipal authorities manage large numbers of infrastructure assets such as roads, bridges, and drainage networks.

Identifying which assets require immediate attention can be difficult when infrastructure information is distributed across different sources and inspection-based decisions are handled manually.

InfraRisk aims to provide a centralized system that can:

- Monitor infrastructure health
- Identify high-risk infrastructure assets
- Classify assets according to their risk
- Prioritize maintenance and repair activities
- Support municipal decision-making
- Provide field inspectors with a structured way to report infrastructure conditions

---

## Solution

InfraRisk processes infrastructure information and calculates health and risk indicators for individual assets and infrastructure networks.

The system currently evaluates infrastructure using factors such as:

- Installation year and expected service life
- Condition score
- Accident history
- Environmental exposure
- Leakage information for drainage infrastructure
- Infrastructure material

These factors are normalized where required and combined using transparent scoring methods to produce infrastructure health indicators.

The resulting information can be used to identify assets requiring greater attention and support repair prioritization.

---

## Main Users

### Municipal Officer

The municipal officer dashboard provides a high-level view of infrastructure across the municipality.

Capabilities include:

- View overall infrastructure health
- Monitor road network health
- Monitor bridge network health
- Monitor drainage network health
- View total infrastructure assets
- Identify high-risk and critical assets
- View asset-level risk information
- Support maintenance and repair planning

### Field Inspector

The field inspector interface is intended for infrastructure-level inspection activities.

Capabilities include:

- View assigned assets
- Record inspection information
- Report infrastructure conditions
- Identify urgent infrastructure issues
- Update inspection status

---

## System Workflow

```text
Infrastructure Data
        ↓
Field Inspection
        ↓
Data Processing
        ↓
Health & Risk Assessment
        ↓
Risk Classification
        ↓
Repair Prioritization
        ↓
Maintenance Planning
        ↓
Municipal Decision


```

Infrastructure Health Assessment

InfraRisk calculates separate health scores for:

Road networks
Bridge networks
Drainage networks

The individual infrastructure health scores are calculated from relevant infrastructure attributes.

For example, road and bridge health currently considers:

Asset age relative to expected life
Accident history
Environmental exposure
Condition score

Drainage health currently considers:

Material
Asset age relative to expected life
Leakage health

The overall infrastructure health is derived from the health scores of the three infrastructure networks.

The scoring system uses equal weights for the current prototype where no reliable domain-specific weighting data was available.

This approach keeps the scoring transparent and avoids assigning unsupported importance to individual factors.

Risk Classification

Assets are classified according to their calculated risk score:

Risk Score	Classification
>= 85	Critical
>= 65 and < 85	High
>= 45 and < 65	Moderate
< 45	Low

This classification allows municipal authorities to quickly identify assets requiring greater attention.

Data
Current Prototype Data

The current prototype uses a combination of available infrastructure data and fabricated/synthetic data.

This was necessary because sufficiently detailed, standardized, and openly accessible datasets containing all required infrastructure attributes were not available during the implementation period.

Where real infrastructure data was available, it was used as the basis for the system. Missing attributes and infrastructure datasets were supplemented with fabricated data so that the complete workflow could be implemented and demonstrated.

The fabricated data is used strictly for prototype and demonstration purposes and should not be interpreted as actual government infrastructure records.

Future Data Integration

A major future objective is to replace the fabricated data with verified infrastructure data obtained from appropriate government and municipal sources.

The system is designed so that the underlying database and processing layer can be updated when reliable datasets become available.

Future data sources may include:

Government open-data portals
Municipal infrastructure databases
Official infrastructure departments
Field inspection records
GIS datasets
Infrastructure monitoring systems
IoT and sensor systems

Data validation and standardization will be performed before integrating external datasets into the production system.

Technology Stack
Frontend
HTML
CSS
JavaScript
Backend
Python
Flask
Database
PostgreSQL
Data Processing
Python
Pandas
Machine Learning

Machine learning components are planned for future risk prediction and infrastructure failure forecasting.

Backend

The backend provides API endpoints for:

Authentication
Dashboard data
Infrastructure health calculation
Asset information
Risk classification
Repair planning

The application uses PostgreSQL for persistent infrastructure and user data.

Authentication uses government-assigned IDs and role information. The backend establishes a session after successful authentication and uses the user's role to determine access to the appropriate dashboard.

### Security Considerations

- Password hashing using Argon2
- Session-based authentication
- Role-based access control
- Generic authentication errors to avoid revealing whether the Government ID or password is incorrect
- Environment variables for sensitive configuration

---

## Key Features

- Government ID-based authentication
- Role-based access
- Municipal officer dashboard
- Field inspector dashboard
- Road health monitoring
- Bridge health monitoring
- Drainage health monitoring
- Asset-level risk assessment
- Risk classification
- High-risk and critical asset identification
- Infrastructure repair prioritization
- PostgreSQL-based infrastructure data management

---

## Project Structure

```text
InfraRisk/
│
├── data/
│   └── infrastructure_data.csv
│
├── login.html
├── dashboard.html
├── assets.html
├── repair-planning.html
├── reports.html
├── style.css
│
├── app.py
├── .gitignore
└── README.md
```
Prototype / Hackathon Project

The current version demonstrates the core architecture and workflow of InfraRisk, including:

User authentication
Role-based dashboard access
PostgreSQL integration
Infrastructure health calculations
Asset risk classification
Municipal infrastructure monitoring

The current prototype uses fabricated data for portions of the infrastructure dataset where suitable public data was unavailable during development.

The scoring methodology is also intended as a transparent prototype approach rather than a validated engineering standard.

Limitations

The current prototype has several limitations:

Some infrastructure attributes use synthetic data
Risk and health scoring formulas have not been validated against historical infrastructure failures
Current scoring weights are equal where reliable domain-specific weights were unavailable
The prototype does not yet integrate directly with government infrastructure databases
Machine learning-based prediction is not yet part of the core implemented workflow
Production deployment would require stronger infrastructure, authentication, authorization, monitoring, and security controls

These limitations are intended to be addressed as the system moves from prototype to production.

#Future Scope
1. Government Data Integration
Replace fabricated infrastructure data with verified data from government and municipal authorities.
The system can be adapted to consume standardized government datasets and APIs when appropriate access is available. Weights of parameters can be altered once the
actual data is available/accessible.

3. GIS Integration
Integrate geographic information systems to display infrastructure assets on interactive maps.
This would allow officers to:
-Analyze nearby critical facilities at a glance
-Locate high-risk assets
-Identify geographical risk clusters
-View infrastructure by district or municipality
-Analyze nearby critical facilities

3. Machine Learning-Based Risk Prediction
Historical inspection, maintenance, accident, and failure data can be used to train machine learning models.
Future models could predict:
Probability of infrastructure failure
Expected deterioration
Future maintenance requirements
Asset-specific risk

ML predictions should be evaluated against historical data before being used for operational decisions.

4. Evidence-Based Risk Weights
The current prototype uses equal weights where reliable evidence for different factor importance was unavailable.
With sufficient historical data, statistical analysis and domain expertise can be used to determine evidence-based weights rather than relying on manually selected values.

5. Real-Time Infrastructure Monitoring
Integration with sensors and IoT devices could provide continuously updated information such as:
Structural condition
Water leakage
Pipeline pressure
Road condition
Environmental exposure

6. Mobile App version
Current version is a web application but future versions can include mobile app format for easier accessibility



#NOTE:
-InfraRisk is currently a prototype developed for demonstration and evaluation purposes.
-The fabricated/synthetic infrastructure data used in the prototype does not represent actual government infrastructure records.
-Before deployment in a real municipal environment, the system would require verified infrastructure data, validated engineering methodologies, domain-expert review, appropriate government authorization, security assessment, and operational testing.

#Project Status
Prototype / Hackathon Project
