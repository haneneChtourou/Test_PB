import json, os

rapports = []
for f in [
    'rapport_login.json',
    'rapport_transfer.json',
    'rapport_find.json',
    'rapport_loan.json',
    'rapport_creation_compte.json',
    'rapport_bill_pay.json'
]:
    if os.path.exists(f):
        with open(f, encoding='utf-8') as file:
            rapports.extend(json.load(file))
        print(f"✅ {f} ajouté")
    else:
        print(f"⚠️ {f} introuvable")

with open('rapport.json', 'w', encoding='utf-8') as f:
    json.dump(rapports, f, ensure_ascii=False, indent=2)

print('✅ rapport.json fusionné !')