# from behave import given, when, then
# from selenium import webdriver
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from behave import given, when, then
# from environment import creer_driver
# import os


# @given("j'ouvre ParaBank")
# def step_open(context):
#     context.driver = creer_driver()
#     context.wait   = WebDriverWait(context.driver, 15)
    
#     # Ouvre la page
#     context.driver.get("https://parabank.parasoft.com/parabank/index.htm")
    
#     # Vérifie qu'on est sur la bonne page
#     if "index.htm" not in context.driver.current_url:
#         print("\n⚠️ Mauvaise page, rechargement...")
#         context.driver.get("https://parabank.parasoft.com/parabank/index.htm")
    
#     # Attend que le champ username soit présent
#     context.wait.until(EC.presence_of_element_located((By.NAME, "username")))
#     print("\n✅ Page de login chargée !")

# @when('je saisis username "{username}" et password "{password}"')
# def step_credentials(context, username, password):
#     field_user = context.wait.until(EC.presence_of_element_located((By.NAME, "username")))
#     field_user.clear()
#     field_user.send_keys(username)

#     field_pass = context.wait.until(EC.presence_of_element_located((By.NAME, "password")))
#     field_pass.clear()
#     field_pass.send_keys(password)


# @when("je clique sur Log In")
# def step_click_login(context):
#     context.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Log In']"))).click()


# @then('je dois voir "Welcome"')
# def step_welcome(context):
#     try:
#         context.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Welcome')]")))
#         print("\n✅ PASSED : CONNEXION REUSSIE !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         context.driver.save_screenshot("screenshots/login_valide_FAILED.png")
#         assert False, "❌ ÉCHEC : 'Welcome' introuvable."
#     finally:
#         context.driver.quit()


# @then("je dois voir un message d'erreur")
# def step_error(context):
#     try:
#         context.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Error')]")))
#         print("\n✅ PASSED : MESSAGE D'ERREUR PRESENT !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         nom = context.scenario.name.replace(" ", "_")
#         context.driver.save_screenshot(f"screenshots/{nom}_FAILED.png")
#         assert False, "❌ ÉCHEC : Message d'erreur introuvable."
#     finally:
#         context.driver.quit()


# from behave import given, when, then
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from environment import creer_driver, BASE_URL
# import os


# @given("j'ouvre ParaBank")
# def step_open(context):
#     context.driver = creer_driver()
#     context.wait   = WebDriverWait(context.driver, 15)
#     context.driver.get(f"{BASE_URL}/index.htm")


# @when('je saisis username "{username}" et password "{password}"')
# def step_credentials(context, username, password):
#     field_user = context.wait.until(EC.presence_of_element_located((By.NAME, "username")))
#     field_user.clear()
#     field_user.send_keys(username)

#     field_pass = context.wait.until(EC.presence_of_element_located((By.NAME, "password")))
#     field_pass.clear()
#     field_pass.send_keys(password)


# @when("je clique sur Log In")
# def step_click_login(context):
#     context.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Log In']"))).click()


# @then('je dois voir "Welcome"')
# def step_welcome(context):
#     try:
#         context.wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//*[contains(text(),'Welcome')]")
#         ))
#         print("\n✅ PASSED : CONNEXION REUSSIE !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         context.driver.save_screenshot("screenshots/login_valide_FAILED.png")
#         assert False, "❌ ÉCHEC : 'Welcome' introuvable."
#     finally:
#         context.driver.quit()


# @then("je dois voir un message d'erreur")
# def step_error(context):
#     try:
#         context.wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//*[contains(text(),'Error')]")
#         ))
#         print("\n✅ PASSED : MESSAGE D'ERREUR PRESENT !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         nom = context.scenario.name.replace(" ", "_")
#         context.driver.save_screenshot(f"screenshots/{nom}_FAILED.png")
#         assert False, "❌ ÉCHEC : Message d'erreur introuvable."
#     finally:
#         context.driver.quit()



from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from environment import creer_driver
import os
import time

# URL spécifique pour login
LOGIN_URL = "https://parabank.parasoft.com/parabank"


@given("j'ouvre ParaBank")
def step_open(context):
    context.driver = creer_driver()
    context.wait   = WebDriverWait(context.driver, 15)
    context.driver.get(f"{LOGIN_URL}/index.htm")
    time.sleep(2)


@when('je saisis username "{username}" et password "{password}"')
def step_credentials(context, username, password):
    field_user = context.wait.until(EC.presence_of_element_located((By.NAME, "username")))
    field_user.clear()
    time.sleep(1)
    field_user.send_keys(username)
    time.sleep(1)

    field_pass = context.wait.until(EC.presence_of_element_located((By.NAME, "password")))
    field_pass.clear()
    time.sleep(1)
    field_pass.send_keys(password)
    time.sleep(1)


@when("je clique sur Log In")
def step_click_login(context):
    time.sleep(1)
    context.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Log In']"))).click()
    time.sleep(2)


@then('je dois voir "Welcome John Smith"')
def step_welcome(context):
    try:
        context.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(.,'Welcome') and contains(.,'John Smith')]")
        ))
        print("\n✅ PASSED : CONNEXION REUSSIE ! → Welcome John Smith")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/login_valide_FAILED.png")
        assert False, "❌ ÉCHEC : 'Welcome John Smith' introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()


@then("je dois voir un message d'erreur")
def step_error(context):
    try:
        context.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Error')]")
        ))
        print("\n✅ PASSED : MESSAGE D'ERREUR PRESENT !")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        nom = context.scenario.name.replace(" ", "_")
        context.driver.save_screenshot(f"screenshots/{nom}_FAILED.png")
        assert False, "❌ ÉCHEC : Message d'erreur introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()