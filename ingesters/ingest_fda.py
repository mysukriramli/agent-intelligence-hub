import logging
import requests
from ingesters.utils import save_feed_data

logger = logging.getLogger("OmniWire.FDA")

def run():
    url = "https://api.fda.gov/drug/enforcement.json?sort=report_date:desc&limit=20"
    try:
        res = requests.get(url, timeout=15)
        res.raise_for_status()
        results = res.json().get("results", [])

        items = []
        md_lines = ["# openFDA Drug Enforcement & Recall Wire", "## Recent Medical Recalls\n"]

        for r in results:
            item = {
                "recall_number": r.get("recall_number"),
                "recalling_firm": r.get("recalling_firm"),
                "product_description": r.get("product_description"),
                "reason_for_recall": r.get("reason_for_recall"),
                "classification": r.get("classification"),
                "report_date": r.get("report_date")
            }
            items.append(item)
            md_lines.append(f"- **[{item['classification']}] {item['recalling_firm']}**: {item['reason_for_recall']} (Reported: {item['report_date']})")

        save_feed_data("fda", "recalls", items, "\n".join(md_lines))
        logger.info(f"FDA wire updated: {len(items)} recalls.")
    except Exception as e:
        logger.error(f"FDA ingestion failed: {e}")
