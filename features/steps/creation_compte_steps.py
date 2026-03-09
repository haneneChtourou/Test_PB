from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from environment import creer_driver, BASE_URL
import os
import time
import json

DELAY = 2


@given("l'utilisateur est connecté à ParaBank pour la création de compte")
def step_login_open_account(context):
    context.driver = creer_driver()
    context.wait   = WebDriverWait(context.driver, 15)

    # Vide les cookies
    context.driver.get("about:blank")
    context.driver.get(BASE_URL)
    context.driver.delete_all_cookies()
    context.driver.execute_script("window.localStorage.clear();")
    context.driver.execute_script("window.sessionStorage.clear();")

    context.driver.get(f"{BASE_URL}/index.htm")
    context.wait.until(EC.presence_of_element_located((By.NAME, "username")))

    field_user = context.driver.find_element(By.NAME, "username")
    field_user.clear()
    field_user.send_keys("john")

    field_pass = context.driver.find_element(By.NAME, "password")
    field_pass.clear()
    field_pass.send_keys("demo")

    context.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Log In']"))).click()
    context.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Open New Account")))
    print(f"\n▶️  Connecté ! Démarrage : {context.scenario.name}")


@given('l\'utilisateur est sur la page "Open New Account"')
def step_open_new_account_page(context):
    try:
        context.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Open New Account")
        )).click()
        context.wait.until(EC.visibility_of_element_located((By.ID, "type")))
        print("\n✅ Page Open New Account ouverte")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/open_account_page_FAILED.png")
        assert False, "❌ FAILED : Page Open New Account introuvable."


@when('il sélectionne le type de compte "{account_type}"')
def step_select_account_type(context, account_type):
    try:
        select = Select(context.wait.until(
            EC.visibility_of_element_located((By.ID, "type"))
        ))
        if account_type == "CHECKING":
            select.select_by_value("0")
        elif account_type == "SAVINGS":
            select.select_by_value("1")
        time.sleep(DELAY)
        print(f"\n✅ Type de compte sélectionné : {account_type}")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/select_type_FAILED.png")
        assert False, f"❌ FAILED : Sélection type '{account_type}' échouée."


@when("il sélectionne le compte source")
def step_select_source_account(context):
    try:
        select = Select(context.wait.until(
            EC.visibility_of_element_located((By.ID, "fromAccountId"))
        ))
        select.select_by_index(0)
        context.source_account = select.first_selected_option.text
        time.sleep(DELAY)
        print(f"\n✅ Compte source sélectionné : {context.source_account}")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/select_source_FAILED.png")
        assert False, "❌ FAILED : Sélection compte source échouée."


@when("il sélectionne un compte source avec solde insuffisant")
def step_select_low_balance_account(context):
    try:
        select = Select(context.wait.until(
            EC.visibility_of_element_located((By.ID, "fromAccountId"))
        ))
        options = select.options
        select.select_by_index(len(options) - 1)
        context.source_account = select.first_selected_option.text
        time.sleep(DELAY)
        print(f"\n✅ Compte source faible solde : {context.source_account}")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/select_low_balance_FAILED.png")
        assert False, "❌ FAILED : Sélection compte faible solde échouée."


@when('il clique sur "Open New Account"')
def step_click_open_account(context):
    try:
        context.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[value='Open New Account']")
        )).click()
        time.sleep(DELAY)
        print("\n✅ Bouton Open New Account cliqué")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/click_open_account_FAILED.png")
        assert False, "❌ FAILED : Bouton Open New Account introuvable."


@then("le nouveau compte Checking doit être créé avec succès")
def step_verify_checking_created(context):
    try:
        context.wait.until(EC.visibility_of_element_located((By.ID, "openAccountResult")))
        time.sleep(DELAY)
        result_title = context.driver.find_element(
            By.CSS_SELECTOR, "#openAccountResult h1"
        ).text
        print(f"\n✅ Résultat : {result_title}")
        assert "Congratulations" in result_title, f"❌ Compte non créé : {result_title}"
        context.new_account_id = context.driver.find_element(By.ID, "newAccountId").text
        print(f"\n✅ PASSED : Compte Checking créé : {context.new_account_id}")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/checking_created_FAILED.png")
        assert False, "❌ FAILED : Création compte Checking échouée."


@then("le nouveau compte Savings doit être créé avec succès")
def step_verify_savings_created(context):
    try:
        context.wait.until(EC.visibility_of_element_located((By.ID, "openAccountResult")))
        time.sleep(DELAY)
        result_title = context.driver.find_element(
            By.CSS_SELECTOR, "#openAccountResult h1"
        ).text
        print(f"\n✅ Résultat : {result_title}")
        assert "Congratulations" in result_title, f"❌ Compte non créé : {result_title}"
        context.new_account_id = context.driver.find_element(By.ID, "newAccountId").text
        print(f"\n✅ PASSED : Compte Savings créé : {context.new_account_id}")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/savings_created_FAILED.png")
        assert False, "❌ FAILED : Création compte Savings échouée."


@then("le numéro du nouveau compte doit être affiché")
def step_verify_account_number(context):
    try:
        new_account = context.driver.find_element(By.ID, "newAccountId").text
        print(f"\n✅ Numéro du nouveau compte : {new_account}")
        assert new_account, "❌ Numéro de compte non affiché !"
        assert new_account.isdigit(), f"❌ Numéro invalide : {new_account}"
        print(f"\n✅ PASSED : Numéro de compte valide : {new_account}")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/account_number_FAILED.png")
        assert False, "❌ FAILED : Numéro de compte introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()


@then('le solde initial doit être supérieur à "{expected_balance}"')
def step_verify_initial_balance(context, expected_balance):
    try:
        new_account_id = context.driver.find_element(By.ID, "newAccountId").text
        print(f"\n✅ Nouveau compte : {new_account_id}")

        context.driver.get(
            f"{BASE_URL}/services_proxy/bank/accounts/{new_account_id}"
        )
        time.sleep(DELAY)

        body         = context.driver.find_element(By.TAG_NAME, "body").text
        account_data = json.loads(body)
        balance      = float(account_data.get("balance", 0))

        print(f"\n✅ Solde initial : {balance}")
        assert balance > float(expected_balance), f"❌ Solde insuffisant : {balance}"
        print(f"\n✅ PASSED : Solde initial valide : {balance}")

        context.driver.back()
        time.sleep(DELAY)
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/initial_balance_FAILED.png")
        assert False, "❌ FAILED : Vérification solde échouée."
    finally:
        time.sleep(2)
        context.driver.quit()


@then("une erreur de solde insuffisant doit s'afficher")
def step_verify_insufficient_balance_error(context):
    try:
        time.sleep(DELAY)
        error_elements = context.driver.find_elements(By.CSS_SELECTOR, ".error")

        if error_elements:
            for error in error_elements:
                if error.is_displayed() and error.text:
                    print(f"\n✅ PASSED : Erreur affichée : {error.text}")
                    return

        result = context.driver.find_elements(By.ID, "openAccountResult")
        if result and result[0].is_displayed():
            title = context.driver.find_element(
                By.CSS_SELECTOR, "#openAccountResult h1"
            ).text
            print(f"\n✅ Résultat : {title}")
            assert "Congratulations" not in title, "❌ Compte créé alors que solde insuffisant !"

        print("\n✅ PASSED : Erreur solde insuffisant détectée !")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/insufficient_balance_FAILED.png")
        assert False, "❌ FAILED : Erreur solde insuffisant introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()