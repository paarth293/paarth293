"""Every link on the profile lives here. Edit, push, and the
`Rebuild profile images` workflow regenerates README.md and every image.
"""

LOGIN = "paarth293"

# Your deployed portfolio. None -> links go to its repository instead.
PORTFOLIO_URL = None

LINKEDIN = "https://www.linkedin.com/in/paarth-gupta-279aab328/"
LEETCODE = "https://leetcode.com/u/Paarth_05/"
EMAIL = "i.m.paarthgupta@gmail.com"
LANGUAGE_METRICS = "https://languagemetrics.in"

# Repositories (verified public on GitHub) and live deployments.
REPOS = {
    "mandateos": "https://github.com/paarth293/MandateOS",
    "clauseguard": "https://github.com/paarth293/ClauseGuard",
    "knowledge-agent": "https://github.com/paarth293/Knowledge-Agent",
    "truebrain": "https://github.com/paarth293/TrueBrain",
    "promptforge": "https://github.com/paarth293/PromptForge",
    "drishti": "https://github.com/TechTonicWavee/Drishti",   # SIH team repo
    "portfolio": "https://github.com/paarth293/Portfolio-Paarth",
}
LIVE = {
    "mandateos": "https://mandate-os-lovat.vercel.app",
    "clauseguard": "https://clause-guard-ruby.vercel.app",
}


def repo(slug: str) -> str:
    return REPOS.get(slug) or f"https://github.com/{LOGIN}?tab=repositories"


def portfolio() -> str:
    return PORTFOLIO_URL or REPOS["portfolio"]
