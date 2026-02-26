from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from environment import creer_driver
import os

# @given("je suis connecté sur ParaBank")
# def step_login(context):
#     options = Options()
#     options.add_argument("--start-maximized")
#     context.driver = webdriver.Edge(options=options)
#     context.wait   = WebDriverWait(context.driver, 15)
#     context.driver.get("https://parabank.parasoft.com/parabank/index.htm")
#     context.wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("john")
#     context.wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("demo")
#     context.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Log In']"))).click()
#     context.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Welcome')]")))
#     print(f"\n▶️  Connecté ! Démarrage : {context.scenario.name}")

@given("je suis connecté sur ParaBank")
def step_login(context):
    context.driver = creer_driver()
    context.wait   = WebDriverWait(context.driver, 15)
    
    # Ouvre la page
    context.driver.get("https://parabank.parasoft.com/parabank/index.htm")
    
    # Vérifie qu'on est sur la bonne page
    if "index.htm" not in context.driver.current_url:
        print("\n⚠️ Mauvaise page, rechargement...")
        context.driver.get("https://parabank.parasoft.com/parabank/index.htm")
    
    # Attend que le champ username soit présent
    context.wait.until(EC.presence_of_element_located((By.NAME, "username")))
    
    # Login
    context.wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("john")
    context.wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("demo")
    context.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Log In']"))).click()
    context.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Welcome')]")))
    print(f"\n▶️  Connecté ! Démarrage : {context.scenario.name}")


@given("je vais sur Transfer Funds")
def step_go_transfer(context):
    context.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))).click()
    field = context.wait.until(EC.element_to_be_clickable((By.ID, "amount")))
    field.click()
    print("\n✅ Page Transfer Funds chargée !")

    # From → premier compte
    context.wait.until(lambda d: len(Select(d.find_element(By.ID, "fromAccountId")).options) > 0)
    from_select = Select(context.driver.find_element(By.ID, "fromAccountId"))
    from_select.select_by_index(0)
    print(f"\n✅ From compte : {from_select.options[0].text}")

    # To → deuxième compte
    context.wait.until(lambda d: len(Select(d.find_element(By.ID, "toAccountId")).options) > 1)
    to_select = Select(context.driver.find_element(By.ID, "toAccountId"))
    to_select.select_by_index(1)
    print(f"\n✅ To compte : {to_select.options[1].text}")


@when('je saisis le montant "{montant}"')
def step_amount(context, montant):
    field = context.wait.until(EC.element_to_be_clickable((By.ID, "amount")))
    field.click()
    field.clear()
    field.send_keys(montant)
    print(f"\n✅ Montant saisi : '{montant}'")


@when("je laisse le montant vide")
def step_amount_vide(context):
    field = context.wait.until(EC.element_to_be_clickable((By.ID, "amount")))
    field.click()
    field.clear()
    print("\n✅ Montant laissé vide")


@when("je clique sur Transfer")
def step_click_transfer(context):
    context.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Transfer']"))).click()


@then('je dois voir "Transfer Complete"')
def step_transfer_success(context):
    try:
        context.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Transfer Complete')]")))
        print("\n✅ PASSED : TRANSFERT REUSSI !")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/transfer_valide_FAILED.png")
        assert False, "❌ ÉCHEC : 'Transfer Complete' introuvable."
    finally:
        context.driver.quit()


@then("je dois voir un message d'erreur transfert")
def step_transfer_error(context):
    try:
        context.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Error') or contains(text(),'error') or contains(text(),'Please')]")))
        print("\n✅ PASSED : MESSAGE D'ERREUR TRANSFERT PRESENT !")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        nom = context.scenario.name.replace(" ", "_")
        context.driver.save_screenshot(f"screenshots/{nom}_FAILED.png")
        assert False, "❌ ÉCHEC : Message d'erreur transfert introuvable."
    finally:
        context.driver.quit()