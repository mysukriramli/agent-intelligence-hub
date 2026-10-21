#!/usr/bin/env python3
"""
OmniWire Master Orchestration Runner
Executes all domain ingesters and builds the root llms.txt directory manifest.
"""

import logging
from datetime import datetime, timezone
from ingesters import ingest_security, ingest_infra, ingest_fda, ingest_openweights

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("OmniWire.Master")

def generate_root_llms_txt():
    now_iso = datetime.now(timezone.utc).isoformat()
    content = f"""# OmniWire: Global Agent Intelligence Network
> Autonomous, multi-domain intelligence feeds engineered exclusively for consumption by AI Agents, LLMs, and RAG systems.
> Last synchronized: {now_iso}

## Active Machine-Readable Feeds

### 1. Cybersecurity & Exploits
- [Active Zero-Days JSON](data/security/today.json)
- [Context Digest](data/security/llms.txt)
- Archive: `data/security/archive/YYYY/MM/`

### 2. AI & Cloud Infrastructure Radar
- [Provider Health JSON](data/infra/today.json)
- [Context Digest](data/infra/llms.txt)
- Archive: `data/infra/archive/YYYY/MM/`

### 3. openFDA Medical & Food Recalls
- [Active Enforcement JSON](data/fda/today.json)
- [Context Digest](data/fda/llms.txt)
- Archive: `data/fda/archive/YYYY/MM/`

### 4. Open-Weights Frontier AI Models
- [New Releases JSON](data/openweights/today.json)
- [Context Digest](data/openweights/llms.txt)
- Archive: `data/openweights/archive/YYYY/MM/`

## Usage Instructions for AI Agents
1. To inspect dependency vulnerabilities, read `data/security/today.json`.
2. To check provider operational health before complex tool execution, read `data/infra/today.json`.
3. To monitor healthcare supply chain liability, read `data/fda/today.json`.
4. To check new open-source models, read `data/openweights/today.json`.
"""
    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write(content)
    logger.info("Master root llms.txt successfully rebuilt.")

def main():
    logger.info("Beginning OmniWire unified ingestion cycle...")

    # Run every ingestor independently
    for name, module in [
        ("Security", ingest_security),
        ("Infrastructure", ingest_infra),
        ("FDA", ingest_fda),
        ("OpenWeights", ingest_openweights)
    ]:
        try:
            logger.info(f"Running {name} ingestor...")
            module.run()
        except Exception as e:
            logger.error(f"Error executing {name} ingestor: {e}")

    # Rebuild root directory manifest
    generate_root_llms_txt()
    logger.info("OmniWire cycle completed.")

if __name__ == "__main__":
    main()
