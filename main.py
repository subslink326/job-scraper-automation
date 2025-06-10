#!/usr/bin/env python3
"""
Job Scraper Automation
----------------------

Usage:
    python main.py --url <JOB_POSTING_URL> --resume <PATH_TO_RESUME>

This script scrapes a job posting URL, extracts relevant information,
and updates the workflow_tasks.json file with the results of each step
in the 20‑step workflow.

NOTE: This is a starter template. Extend each `step_*` function
with the actual logic you need.
"""

import argparse
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup

WORKFLOW_FILE = Path("workflow_tasks.json")


def scrape_job_post(url: str) -> str:
    """Fetch and return the raw HTML of the job posting."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


def parse_job_post(html: str) -> dict:
    """Extract key fields from the job posting (placeholder implementation)."""
    soup = BeautifulSoup(html, "html.parser")
    return {
        "title": soup.title.string if soup.title else "",
        "raw_html": html,
    }


def load_workflow() -> list:
    with WORKFLOW_FILE.open() as f:
        return json.load(f)


def save_workflow(data: list) -> None:
    with WORKFLOW_FILE.open("w") as f:
        json.dump(data, f, indent=2)


def step_1_analyze_job_posting(job_data: dict, workflow: list):
    """Populate step 1 output with a summary of the job posting."""
    summary = f"Title: {job_data.get('title')}"
    workflow[0]["output"] = summary


def main():
    parser = argparse.ArgumentParser(description="Job Scraper Automation")
    parser.add_argument("--url", required=True, help="Job posting URL")
    parser.add_argument("--resume", required=False, help="Path to resume file")
    args = parser.parse_args()

    html = scrape_job_post(args.url)
    job_data = parse_job_post(html)

    workflow = load_workflow()
    step_1_analyze_job_posting(job_data, workflow)
    save_workflow(workflow)

    print("Step 1 completed and saved to workflow_tasks.json")


if __name__ == "__main__":
    main()
