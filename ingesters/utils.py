import os
import json
from datetime import datetime, timezone

def save_feed_data(domain: str, payload_key: str, items: list, markdown_brief: str):
    """
    Saves data to data/{domain}/today.json, data/{domain}/llms.txt,
    and archives to data/{domain}/archive/YYYY/MM/YYYY-MM-DD.json.
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    year_str = now.strftime("%Y")
    month_str = now.strftime("%m")

    base_dir = os.path.join("data", domain)
    archive_dir = os.path.join(base_dir, "archive", year_str, month_str)
    os.makedirs(archive_dir, exist_ok=True)

    today_json_path = os.path.join(base_dir, "today.json")
    llms_txt_path = os.path.join(base_dir, "llms.txt")
    archive_json_path = os.path.join(archive_dir, f"{date_str}.json")

    payload = {
        "metadata": {
            "domain": domain,
            "generated_at": now.isoformat(),
            "total_items": len(items),
            "schema_version": "1.0.0"
        },
        payload_key: items
    }

    # 1. Write today.json (rolling active state)
    with open(today_json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    # 2. Write domain-specific llms.txt
    with open(llms_txt_path, "w", encoding="utf-8") as f:
        f.write(markdown_brief)

    # 3. Write / append to daily historical archive
    with open(archive_json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
