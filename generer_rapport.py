import json

with open("rapport.json", encoding="utf-8") as f:
    data = json.load(f)

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rapport de Tests ParaBank</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background: #f5f5f5; }
        h1   { color: #333; text-align: center; }
        h2   { color: #555; margin-top: 30px; }
        .passed  { background: #d4edda; border-left: 5px solid #28a745; }
        .failed  { background: #f8d7da; border-left: 5px solid #dc3545; }
        .error   { background: #fff3cd; border-left: 5px solid #ffc107; }
        .scenario { padding: 10px 15px; margin: 10px 0; border-radius: 4px; }
        .step  { margin: 5px 20px; font-size: 14px; color: #444; }
        .step.passed { background: none; border: none; color: #28a745; }
        .step.failed { background: none; border: none; color: #dc3545; }
        .step.error  { background: none; border: none; color: #ffc107; }
        .badge { float: right; padding: 2px 8px; border-radius: 10px; font-size: 12px; color: white; }
        .badge.passed { background: #28a745; }
        .badge.failed { background: #dc3545; }
        .badge.error  { background: #ffc107; color: #333; }
        .summary { text-align: center; padding: 20px; background: white; border-radius: 8px; margin-bottom: 20px; }
        .summary span { margin: 0 15px; font-size: 18px; font-weight: bold; }
        .duration { font-size: 12px; color: #999; float: right; }
    </style>
</head>
<body>
<h1>🧪 Rapport de Tests ParaBank</h1>
"""

total_scenarios = 0
passed_scenarios = 0
failed_scenarios = 0
error_scenarios  = 0

for feature in data:
    html += f"<h2>📋 {feature['name']}</h2>"
    for element in feature.get("elements", []):
        if element["type"] == "background":
            continue
        status  = element.get("status", "unknown")
        name    = element["name"]
        total_scenarios += 1
        if status == "passed":
            passed_scenarios += 1
        elif status == "failed":
            failed_scenarios += 1
        else:
            error_scenarios += 1

        html += f"""
        <div class="scenario {status}">
            <strong>{name}</strong>
            <span class="badge {status}">{status.upper()}</span>
            <br>
        """
        for step in element.get("steps", []):
            step_status   = step.get("result", {}).get("status", "skipped")
            step_duration = step.get("result", {}).get("duration", 0)
            step_name     = f"{step['keyword']} {step['name']}"
            html += f"""
            <div class="step {step_status}">
                {'✅' if step_status == 'passed' else '❌' if step_status == 'failed' else '⚠️' if step_status == 'error' else '⏭️'}
                {step_name}
                <span class="duration">{step_duration:.2f}s</span>
            </div>
            """
        html += "</div>"

html += f"""
<div class="summary">
    <span style="color:#28a745">✅ Passed : {passed_scenarios}</span>
    <span style="color:#dc3545">❌ Failed : {failed_scenarios}</span>
    <span style="color:#ffc107">⚠️ Error  : {error_scenarios}</span>
    <span style="color:#333">📊 Total  : {total_scenarios}</span>
</div>
</body>
</html>
"""

with open("rapport.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ rapport.html généré !")