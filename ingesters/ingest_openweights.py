import logging
import requests
from ingesters.utils import save_feed_data

logger = logging.getLogger("OmniWire.OpenWeights")

def run():
    url = "https://huggingface.co/api/models?sort=lastModified&direction=-1&limit=25&full=false"
    try:
        res = requests.get(url, timeout=15)
        res.raise_for_status()
        models = res.json()

        items = []
        md_lines = ["# Open-Weights & Frontier Model Wire", "## Recently Published Hugging Face Models\n"]

        for m in models:
            item = {
                "model_id": m.get("id"),
                "last_modified": m.get("lastModified"),
                "likes": m.get("likes", 0),
                "downloads": m.get("downloads", 0),
                "pipeline_tag": m.get("pipeline_tag", "unknown")
            }
            items.append(item)
            md_lines.append(f"- **{item['model_id']}** (`{item['pipeline_tag']}`): {item['likes']} likes, {item['downloads']} downloads (Updated: {item['last_modified']})")

        save_feed_data("openweights", "models", items, "\n".join(md_lines))
        logger.info(f"OpenWeights wire updated: {len(items)} models.")
    except Exception as e:
        logger.error(f"OpenWeights ingestion failed: {e}")
