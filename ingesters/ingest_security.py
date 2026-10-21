import logging
import requests
from ingesters.utils import save_feed_data

logger = logging.getLogger("OmniWire.Security")

def run():
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    try:
        res = requests.get(url, timeout=15)
        res.raise_for_status()
        vulnerabilities = res.json().get("vulnerabilities", [])[-25:]
        
        items = []
        md_lines = ["# Security Exploit Wire (CISA KEV)", "## Active Zero-Days and Exploits\n"]

        for v in reversed(vulnerabilities):
            item = {
                "cve_id": v.get("cveID"),
                "vendor": v.get("vendorProject"),
                "product": v.get("product"),
                "vulnerability_name": v.get("vulnerabilityName"),
                "date_added": v.get("dateAdded"),
                "action": v.get("requiredAction"),
                "ransomware": v.get("knownRansomwareCampaignUse")
            }
            items.append(item)
            md_lines.append(f"- **[{item['cve_id']}] {item['vendor']} - {item['product']}**: {item['vulnerability_name']} (Added: {item['date_added']}, Ransomware: {item['ransomware']})")

        save_feed_data("security", "vulnerabilities", items, "\n".join(md_lines))
        logger.info(f"Security wire updated: {len(items)} CVEs.")
    except Exception as e:
        logger.error(f"Security ingestion failed: {e}")
