import logging
import requests
from ingesters.utils import save_feed_data

logger = logging.getLogger("OmniWire.Infra")

STATUS_ENDPOINTS = {
    "OpenAI": "https://status.openai.com/api/v2/summary.json",
    "Anthropic": "https://status.anthropic.com/api/v2/summary.json",
    "GitHub": "https://www.githubstatus.com/api/v2/summary.json",
    "Cloudflare": "https://www.cloudflarestatus.com/api/v2/summary.json"
}

def run():
    items = []
    md_lines = ["# AI & Cloud Infrastructure Status Wire", "## Provider System Health\n"]

    for name, url in STATUS_ENDPOINTS.items():
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                overall = data.get("status", {}).get("description", "Unknown")
                incidents = data.get("incidents", [])
                active_incidents = [
                    {"name": inc.get("name"), "status": inc.get("status"), "impact": inc.get("impact")}
                    for inc in incidents if inc.get("status") != "resolved"
                ]

                item = {
                    "provider": name,
                    "overall_status": overall,
                    "active_incidents": active_incidents
                }
                items.append(item)
                inc_desc = f"{len(active_incidents)} ongoing incident(s)" if active_incidents else "Operational"
                md_lines.append(f"- **{name}**: {overall} ({inc_desc})")
        except Exception as e:
            logger.warning(f"Failed to check {name}: {e}")

    save_feed_data("infra", "providers", items, "\n".join(md_lines))
    logger.info("Infra wire updated.")
