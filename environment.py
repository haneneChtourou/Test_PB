# import os
# from selenium import webdriver


# def creer_driver():
#     """Crée Edge en local ou Chrome en CI/CD."""
#     if os.environ.get("CI"):
#         from selenium.webdriver.chrome.options import Options
#         from selenium.webdriver.chrome.service import Service
#         from webdriver_manager.chrome import ChromeDriverManager
#         options = Options()
#         options.add_argument("--headless")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         options.add_argument("--window-size=1280,800")
#         return webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=options
#         )
#     else:
#         from selenium.webdriver.edge.options import Options
#         options = Options()
#         options.add_argument("--start-maximized")
#         return webdriver.Edge(options=options)



import os
from selenium import webdriver

# ── URL de base ───────────────────────────────────────
# Local → localhost, CI → parasoft.com
if os.environ.get("CI"):
    BASE_URL = "https://parabank.parasoft.com/parabank"
else:
    BASE_URL = "http://localhost:8080/parabank"


def creer_driver():
    """Crée Edge en local ou Chrome en CI/CD."""
    if os.environ.get("CI"):
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,800")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    else:
        from selenium.webdriver.edge.options import Options
        options = Options()
        options.add_argument("--start-maximized")
        return webdriver.Edge(options=options)