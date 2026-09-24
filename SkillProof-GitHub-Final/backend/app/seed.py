from sqlalchemy.orm import Session
from .models import Task


def workspace_for(skill, subject):
    key = f"{skill} {subject}".lower()
    if any(x in key for x in ["python", "java", "programming", "web development", "html/css/js"]): return "python" if "python" in key else "java" if "java" in key else "coding"
    if "sql" in key or "database" in key: return "sql"
    if "power bi" in key or "dashboard" in key: return "dashboard"
    if any(x in key for x in ["excel", "accounting", "finance"]): return "accounting" if "accounting" in key else "spreadsheet"
    if any(x in key for x in ["physics", "mechanics", "electronics", "optics", "electromagnetism", "experimental physics", "circuit"]): return "physics"
    if any(x in key for x in ["chemistry", "titration", "reaction", "chemical", "rate experiment"]): return "lab"
    if any(x in key for x in ["statistics", "numerical", "optimization", "mathematics"]): return "math"
    if any(x in key for x in ["marketing", "business", "operations", "human resources", "hr analytics"]): return "business"
    if any(x in key for x in ["design", "visual communication", "canva"]): return "design"
    if any(x in key for x in ["english", "communication", "content"]): return "writing"
    if any(x in key for x in ["biotechnology", "bioinformatics", "microbiology", "laboratory"]): return "lab"
    return "general"


def task(course, subject, skill, title, difficulty, minutes, description, scenario, requirements, resource, starter_code, criteria=None):
    return dict(course=course, subject=subject, skill=skill, title=title, workspace_type=workspace_for(skill, subject), difficulty=difficulty,
                estimated_minutes=minutes, description=description, scenario=scenario,
                requirements=requirements, resource=resource, starter_code=starter_code,
                evaluation_criteria=criteria or {"Correctness":"Strong","Approach":"Good","Problem Solving":"Strong","Understanding":"Good"})

TASKS = [
# Data / computing
 task("B.Sc Data Science","Python","Python","Student Data Cleaner","Intermediate",35,"Clean a messy student dataset and explain data-quality decisions.","A college office received a student CSV containing duplicates and missing attendance values.",["Inspect before changing","Handle duplicates","Handle missing values","Explain one decision"],"students_messy.csv","import pandas as pd\n\ndf = pd.read_csv('students_messy.csv')\nprint(df.head())\nprint(df.isna().sum())\n\n# Your work below\n"),
 task("B.Sc Data Science","Statistics","Statistics","Survey Sampling Check","Intermediate",40,"Investigate whether a survey sample is representative.","A student survey has age and department information and the team wants to understand sampling bias.",["Profile the sample","Compare groups","Identify one possible bias","State a limitation"],"survey.csv","# Statistics investigation\n# Record calculations and reasoning here\n"),
 task("B.Sc Data Science","Data Visualization","Power BI","Sales Insight Dashboard","Intermediate",50,"Analyse sales data and create a decision-ready dashboard.","A retail manager needs a compact view of revenue, profit and category performance.",["Identify KPIs","Find two trends","Explain an unusual pattern","Design a decision-ready dashboard"],"sales_2026.csv","# Power BI task\n# Document preparation and dashboard decisions here.\n"),
 task("B.Sc Data Science","SQL","SQL","Customer Retention Query","Advanced",55,"Investigate repeat purchasing behaviour with SQL.","A store wants to identify customers who returned after their first purchase.",["Inspect schema","Identify first purchases","Find repeat behaviour","Explain edge cases"],"retention.db","-- Start by exploring the schema.\nSELECT * FROM orders LIMIT 10;\n"),
 task("B.Sc Data Science","Excel","Excel","Budget Investigation","Beginner",30,"Analyse six months of spending and identify cost-saving insights.","A student club wants to understand where its monthly budget is going.",["Clean the table","Calculate category totals","Find largest cost driver","Give two evidence-based recommendations"],"club_budget.xlsx","# Excel work notes\n# Record formulas and findings here.\n"),
 task("B.Sc Data Science","Machine Learning","Machine Learning","Churn Feature Investigation","Advanced",60,"Explore which customer features may be associated with churn before modeling.","A subscription team wants evidence for which variables deserve further investigation.",["Inspect target balance","Compare two features","Avoid leakage","Propose one next experiment"],"customers.csv","# ML investigation\n# Write your reasoning before modeling.\n"),
 task("BCA","Programming","Python","Library Borrowing Analyzer","Intermediate",40,"Analyse borrowing records to identify usage patterns.","A college library wants to know which categories and periods have the highest borrowing activity.",["Inspect dates","Group by category","Find a useful pattern","Explain one limitation"],"library.csv","import pandas as pd\n\ndf = pd.read_csv('library.csv')\nprint(df.head())\n"),
 task("BCA","Database Management","SQL","College Database Investigation","Intermediate",45,"Query student and course tables to answer operational questions.","An administrator needs evidence about enrollment and course participation.",["Inspect tables","Use a join","Filter meaningfully","Explain what the query proves"],"college.db","-- Inspect the database first.\nSELECT name FROM sqlite_master WHERE type='table';\n"),
 task("BCA","Web Development","HTML/CSS/JS","Accessible Student Portal Page","Intermediate",50,"Build a responsive portal page with clear structure and accessibility.","A college club needs a simple event page that works on mobile and desktop.",["Create semantic structure","Add responsive layout","Provide accessible labels","Explain one design decision"],"portal-brief.pdf","<!-- Start your page structure here -->\n"),

# Commerce / business
 task("B.Com","Financial Accounting","Accounting","Bank Reconciliation Investigation","Intermediate",45,"Prepare and explain a bank reconciliation from two records.","A small business has differences between its cash book and bank statement.",["Classify differences","Prepare reconciliation","Check arithmetic","Explain one adjustment"],"bank_reconciliation.xlsx","# Accounting work\n# Record your reconciliation logic and calculations.\n"),
 task("B.Com","Cost Accounting","Cost Accounting","Product Cost Analysis","Intermediate",45,"Analyse direct and indirect costs for a small product line.","A manufacturer wants to understand which cost components drive unit cost.",["Classify costs","Calculate unit cost","Compare products","Explain a cost driver"],"product_costs.xlsx","# Cost accounting investigation\n"),
 task("B.Com","Financial Management","Finance","Working Capital Investigation","Advanced",50,"Assess working-capital movements and identify a business risk.","A retailer has monthly receivables, inventory and payables data.",["Calculate relevant ratios","Compare periods","Identify one risk","Suggest a testable action"],"working_capital.xlsx","# Finance investigation\n"),
 task("B.Com","Business Analytics","Excel","Retail Sales Investigation","Intermediate",40,"Use Excel to identify useful patterns in monthly sales.","A retailer wants to understand category and regional performance.",["Clean data","Use formulas/pivots","Compare groups","Write two evidence-based findings"],"retail_sales.xlsx","# Excel analysis notes\n"),
 task("B.Com","Marketing","Data Analysis","Campaign Performance Review","Intermediate",40,"Evaluate campaign spend, clicks and conversions.","A marketing team wants to understand which campaigns deserve further testing.",["Calculate rates","Compare campaigns","Flag a misleading metric","Propose one hypothesis"],"campaigns.csv","# Marketing analysis\n"),

# BBA
 task("BBA","Marketing Management","Marketing Analytics","Customer Segmentation Brief","Intermediate",45,"Create an evidence-based customer segmentation recommendation.","A small brand has customer purchase and engagement data.",["Define segments","Use evidence","Avoid unsupported assumptions","Propose a validation step"],"customers.csv","# Segmentation notes\n"),
 task("BBA","Operations","Operations Analytics","Inventory Reorder Investigation","Intermediate",45,"Investigate stock levels and propose a reorder rule.","An operations manager wants to reduce stockouts without over-ordering.",["Inspect demand","Find risky items","Define a rule","State assumptions"],"inventory.xlsx","# Operations investigation\n"),
 task("BBA","Human Resources","HR Analytics","Employee Attrition Clues","Intermediate",45,"Analyse employee data to identify patterns worth investigating.","HR wants to understand department and tenure patterns without treating correlation as causation.",["Calculate attrition rate","Compare groups","Identify a pattern","State a limitation"],"employees.csv","# HR analytics notes\n"),

# Chemistry
 task("B.Sc Chemistry","Analytical Chemistry","Laboratory Data Analysis","Titration Data Quality Check","Intermediate",50,"Analyse titration readings and identify inconsistent observations.","A laboratory record contains repeated readings for an unknown sample.",["Check units","Calculate a summary","Identify an outlier","Explain whether to retain it"],"titration.csv","# Record calculations and reasoning\n"),
 task("B.Sc Chemistry","Organic Chemistry","Reaction Analysis","Reaction Yield Investigation","Intermediate",45,"Compare theoretical and actual yield and explain the gap.","A lab group recorded reactant mass and isolated product mass.",["Calculate theoretical yield","Calculate percentage yield","Check units","Discuss one plausible loss"],"reaction_data.xlsx","# Organic chemistry calculation\n"),
 task("B.Sc Chemistry","Inorganic Chemistry","Chemical Data Interpretation","Complex Ion Observation Report","Beginner",30,"Turn observations into a structured interpretation.","A practical session produced colour, solubility and reaction observations.",["Organise observations","Separate observation from inference","Identify evidence","State one uncertainty"],"lab_observations.pdf","# Observation -> inference notes\n"),
 task("B.Sc Chemistry","Physical Chemistry","Data Analysis","Rate Experiment Analysis","Advanced",55,"Analyse concentration and time measurements from a rate experiment.","A laboratory team wants to estimate a trend from repeated measurements.",["Inspect data","Choose a suitable transformation","Compare trend","Explain limitation"],"rate_experiment.csv","# Rate experiment analysis\n"),

# Physics
 task("B.Sc Physics","Mechanics","Experimental Physics","Projectile Motion Data Analysis","Intermediate",50,"Analyse measured projectile motion data and compare it with the model.","A lab group measured range and launch conditions across trials.",["Check units","Calculate expected values","Compare measurements","Discuss experimental error"],"projectile.csv","# Physics analysis\n"),
 task("B.Sc Physics","Electronics","Circuit Analysis","Resistor Network Investigation","Intermediate",45,"Analyse voltage/current measurements from a resistor network.","A lab record contains measurements for several circuit configurations.",["Check units","Calculate expected relation","Compare observations","Identify one error source"],"circuit_data.csv","# Circuit investigation\n"),
 task("B.Sc Physics","Optics","Experimental Physics","Lens Experiment Check","Intermediate",45,"Investigate focal-length measurements from an optics experiment.","A set of object and image distances was recorded in a lab.",["Inspect measurements","Apply the relevant relation","Compare trials","Explain uncertainty"],"lens_data.csv","# Optics analysis\n"),
 task("B.Sc Physics","Electromagnetism","Data Analysis","Magnetic Field Measurement Review","Advanced",55,"Analyse field measurements against distance and identify deviations.","A sensor recorded magnetic field strength at different distances.",["Plot the relationship","Identify deviations","Compare with expected trend","Discuss possible causes"],"magnetic_field.csv","# Electromagnetism investigation\n"),

# Mathematics
 task("B.Sc Mathematics","Statistics","Statistics","Survey Descriptive Analysis","Beginner",35,"Summarise a dataset using appropriate descriptive statistics.","A department wants a clear summary of student survey responses.",["Choose suitable measures","Compare mean and median","Identify spread","Explain one limitation"],"survey.csv","# Statistics notes\n"),
 task("B.Sc Mathematics","Operations Research","Optimization","Resource Allocation Scenario","Advanced",60,"Formulate and analyse a simple resource allocation problem.","A small organisation has limited hours and wants to allocate them across activities.",["Define variables","State constraints","Define objective","Interpret the result"],"allocation.xlsx","# Optimization formulation\n"),
 task("B.Sc Mathematics","Numerical Methods","Numerical Analysis","Root-Finding Investigation","Advanced",55,"Compare numerical approaches for finding a root.","A function has a root in a known interval and the team wants to compare convergence behaviour.",["Define the interval","Apply a method","Compare iterations","Explain stopping criteria"],"function.txt","# Numerical methods work\n"),

# General science / biotech
 task("B.Sc Biotechnology","Bioinformatics","Data Analysis","Gene Expression Pattern Review","Advanced",60,"Explore a small gene-expression table and identify patterns worth further study.","A research group has expression measurements across sample groups.",["Check data structure","Compare groups","Identify one pattern","State one biological caution"],"expression.csv","# Bioinformatics investigation\n"),
 task("B.Sc Biotechnology","Microbiology","Laboratory Data Analysis","Growth Curve Investigation","Intermediate",50,"Analyse measurements from a microbial growth experiment.","A lab recorded optical density over time.",["Plot the trend","Identify phases","Compare replicates","Discuss one limitation"],"growth_curve.csv","# Growth curve analysis\n"),

# Communication / design
 task("BA English","Communication Skills","Content Design","Research Summary for Students","Beginner",30,"Turn source notes into a clear student-facing summary.","A student club has research notes that need to become an accurate one-page explainer.",["Identify key claims","Separate evidence from opinion","Use clear structure","Explain one editing decision"],"research_notes.pdf","# Drafting notes\n"),
 task("B.Des","Visual Communication","Canva","Campaign Creative Brief","Beginner",25,"Turn a product brief into a clear social campaign concept.","A student startup needs a simple campaign concept for three social posts.",["Define audience","Create visual direction","Write three content ideas","Explain design choices"],"campaign_brief.pdf","# Creative concept and design reasoning\n"),
]


def seed(db: Session):
    if db.query(Profile).count() == 0:
        db.add(Profile(name="Abdul Baseeth", degree="B.Sc Data Science", college="Student", email="student@example.com",
                       about="Data science student building practical, evidence-based skills.", registered=False))
    if db.query(Task).count() == 0:
        db.add_all([Task(**t) for t in TASKS])
    db.commit()
