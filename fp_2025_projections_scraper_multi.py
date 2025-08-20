#!/usr/bin/env python3
"""
FantasyPros Projections Scraper (2025) — PPR, Half-PPR, Standard
----------------------------------------------------------------
Creates three CSVs with columns:
    Player, Position, Points, Team

Outputs (by default on Windows):
    D:\Programming\FF Drafter\player_rankings_PPR.csv
    D:\Programming\FF Drafter\player_rankings_half_PPR.csv
    D:\Programming\FF Drafter\player_rankings_standard.csv

Notes:
- Uses Firefox (Selenium + geckodriver) when needed, with a fast requests fallback.
- No ADP column anymore (per request).

Install deps (one time):
    pip install selenium geckodriver-autoinstaller pandas lxml beautifulsoup4

Run (headless Firefox):
    python fp_2025_projections_scraper_multi.py --headless

Optional:
    --outdir "C:\some\folder"
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from typing import Dict, List, Optional

import pandas as pd
from bs4 import BeautifulSoup

# ---- Selenium / Firefox setup ----

def ensure_firefox_driver(headless: bool = True):
    """
    Prepare a Firefox Selenium driver using geckodriver_autoinstaller.
    Returns (driver or None, error_message_or_None).
    """
    try:
        import geckodriver_autoinstaller  # type: ignore
        from selenium import webdriver  # type: ignore
        from selenium.webdriver.firefox.options import Options  # type: ignore

        geckodriver_autoinstaller.install()

        options = Options()
        if headless:
            options.add_argument("-headless")
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("media.volume_scale", "0.0")

        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(45)
        return driver, None
    except Exception as e:
        return None, f"Selenium/Firefox init failed: {e}"

def accept_cookies_if_present(driver):
    """Best-effort cookie accept to avoid blocked tables."""
    try:
        from selenium.webdriver.common.by import By  # type: ignore
        from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
        from selenium.webdriver.support import expected_conditions as EC  # type: ignore

        for text in ("Accept All", "I Accept", "Agree", "Accept all cookies"):
            try:
                btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[contains(translate(., 'ACEPTLKOID', 'aceptlkoi d'), '{text.lower()}')]"))
                )
                btn.click()
                time.sleep(0.25)
                break
            except Exception:
                continue
    except Exception:
        pass

def get_html_with_selenium(url: str, headless: bool = True) -> Optional[str]:
    driver, err = ensure_firefox_driver(headless=headless)
    if err:
        print(err, file=sys.stderr)
        return None
    try:
        driver.get(url)
        accept_cookies_if_present(driver)
        from selenium.webdriver.common.by import By  # type: ignore
        from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
        from selenium.webdriver.support import expected_conditions as EC  # type: ignore

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(0.5)
        return driver.page_source
    finally:
        try:
            driver.quit()
        except Exception:
            pass

# ---- Fetch + Parse helpers ----

POS_SLUG = {"QB": "qb", "RB": "rb", "WR": "wr", "TE": "te"}
# FantasyPros scoring param values are typically: PPR, HALF, STD
PROJ_URL = "https://www.fantasypros.com/nfl/projections/{pos}.php?scoring={scoring}&week=draft"

def robust_fetch(url: str, headless: bool = True) -> Optional[str]:
    """Try requests, fall back to Selenium if necessary."""
    try:
        import requests
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0"}
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.ok and ("<table" in resp.text.lower()):
            return resp.text
    except Exception:
        pass
    return get_html_with_selenium(url, headless=headless)

def extract_table_by_headers(soup: BeautifulSoup, required_headers: List[str]) -> Optional[pd.DataFrame]:
    """Find a table whose headers contain all required_headers (case-insensitive)."""
    tables = soup.find_all("table")
    for t in tables:
        try:
            df = pd.read_html(str(t))[0]
        except ValueError:
            continue
        cols_l = [str(c).lower() for c in df.columns]
        if all(any(rh.lower() in c for c in cols_l) for rh in required_headers):
            return df
    return None

def parse_projections(html: str, position: str) -> pd.DataFrame:
    """
    Parse projections table for one position into DataFrame with columns:
    Player, Team, Points, Position
    """
    soup = BeautifulSoup(html, "lxml")
    df = extract_table_by_headers(soup, required_headers=["player", "fpts"])
    if df is None:
        tables = pd.read_html(html)
        if not tables:
            raise RuntimeError(f"Could not find a projections table for {position}.")
        df = max(tables, key=lambda d: d.shape[1])

    pts_col = next((c for c in df.columns if str(c).strip().lower() in ("fpts", "pts", "points", "ppr")), None)
    if pts_col is None:
        numeric_cols = [c for c in df.columns if re.search(r"fpts|points|pts|ppr", str(c), re.I)]
        pts_col = numeric_cols[0] if numeric_cols else df.columns[-1]

    player_col = next((c for c in df.columns if "player" in str(c).lower()), df.columns[0])
    team_col = next((c for c in df.columns if str(c).strip().lower() in ("team", "tm")), None)

    out = []
    for _, row in df.iterrows():
        raw_player = str(row[player_col]).strip()
        if not raw_player or raw_player.lower() == "nan":
            continue

        team = ""
        if team_col is not None and team_col in df.columns:
            team = str(row[team_col]).strip() if pd.notna(row[team_col]) else ""
        else:
            m = re.search(r"\b([A-Z]{2,3})$", raw_player)
            if m:
                team = m.group(1)
                raw_player = raw_player[: m.start()].strip()

        pts_val = row.get(pts_col, None)
        try:
            pts = float(str(pts_val).replace(",", "").strip())
        except Exception:
            m2 = re.search(r"[\d\.]+", str(pts_val))
            pts = float(m2.group()) if m2 else None

        out.append({"Player": raw_player, "Team": team, "Points": pts, "Position": position})

    return pd.DataFrame(out, columns=["Player", "Position", "Points", "Team"])

def build_scoring_csv(scoring_code: str, out_path: str, headless: bool = True) -> pd.DataFrame:
    """Scrape all positions for a scoring code (PPR/HALF/STD) and write CSV."""
    frames = []
    for pos, slug in POS_SLUG.items():
        url = PROJ_URL.format(pos=slug, scoring=scoring_code)
        html = robust_fetch(url, headless=headless)
        if not html:
            raise RuntimeError(f"Failed to fetch projections HTML for {pos} ({scoring_code}).")
        proj = parse_projections(html, position=pos)
        frames.append(proj)

    all_proj = pd.concat(frames, ignore_index=True)

    with pd.option_context("mode.use_inf_as_na", True):
        all_proj["Points"] = pd.to_numeric(all_proj["Points"], errors="coerce")

    all_proj.sort_values(["Position", "Points"], ascending=[True, False], inplace=True, ignore_index=True)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    all_proj.to_csv(out_path, index=False)
    return all_proj

def main():
    parser = argparse.ArgumentParser(description="FantasyPros projections (2025) to CSV for PPR, Half-PPR, and Standard (no ADP).")
    parser.add_argument("--headless", action="store_true", help="Run Firefox in headless mode")
    parser.add_argument("--outdir", default=r"D:\Programming\FF Drafter", help="Directory to write CSV files")
    args = parser.parse_args()

    targets = {
        "PPR": "player_rankings_PPR.csv",
        "HALF": "player_rankings_half_PPR.csv",
        "STD": "player_rankings_standard.csv",
    }

    for scoring, fname in targets.items():
        out_path = os.path.join(args.outdir, fname)
        df = build_scoring_csv(scoring, out_path, headless=args.headless)
        print(f"[{scoring}] Wrote {len(df)} rows to {out_path}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Canceled.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
