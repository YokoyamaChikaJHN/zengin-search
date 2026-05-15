import json
from zengin_code import Bank

data = {}
for bank_code, bank in Bank.all.items():
    branches = {}
    for branch_code, branch in bank.branches.items():
        branches[branch_code] = {
            "code": branch_code,
            "name": branch.name,
            "kana": branch.kana,
            "hira": branch.hira,
            "roma": branch.roma,
        }
    data[bank_code] = {
        "code": bank_code,
        "name": bank.name,
        "kana": bank.kana,
        "hira": bank.hira,
        "roma": bank.roma,
        "branches": branches,
    }

with open("banks.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"エクスポート完了: {len(data)} 銀行")
total_branches = sum(len(b["branches"]) for b in data.values())
print(f"支店合計: {total_branches} 支店")
