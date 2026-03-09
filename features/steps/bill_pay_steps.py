from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from environment import creer_driver, BASE_URL
import os
import time

DELAY = 2


# ==========================
# GIVEN
# ==========================
@given("l'utilisateur est connecté à ParaBank pour le paiement de factures")
def step_login_bill_pay(context):
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
    context.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Bill Pay")))
    print(f"\n▶️  Connecté ! Démarrage : {context.scenario.name}")


@given('l\'utilisateur est sur la page "Bill Pay"')
def step_open_bill_pay(context):
    try:
        context.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Bill Pay")
        )).click()
        context.wait.until(EC.visibility_of_element_located((By.NAME, "payee.name")))
        print("\n✅ Page Bill Pay ouverte")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/bill_pay_page_FAILED.png")
        assert False, "❌ FAILED : Page Bill Pay introuvable."


# ==========================
# WHEN
# ==========================
def saisir_champ(driver, name, value):
    """Saisit une valeur dans un champ via JavaScript."""
    field = driver.find_element(By.NAME, name)
    driver.execute_script("arguments[0].value = '';", field)
    if value:
        driver.execute_script("arguments[0].value = arguments[1];", field, value)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", field)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", field)
    time.sleep(0.3)
    print(f"  ✅ {name} = '{field.get_attribute('value')}'")


@when("il remplit le formulaire avec les données suivantes")
def step_fill_form(context):
    try:
        row = context.table[0]

        saisir_champ(context.driver, "payee.name",            row["payee"])
        saisir_champ(context.driver, "payee.address.street",  row["address"])
        saisir_champ(context.driver, "payee.address.city",    row["city"])
        saisir_champ(context.driver, "payee.address.state",   row["state"])
        saisir_champ(context.driver, "payee.address.zipCode", row["zipCode"])
        saisir_champ(context.driver, "payee.phoneNumber",     row["phone"])
        saisir_champ(context.driver, "payee.accountNumber",   row["account"])
        saisir_champ(context.driver, "verifyAccount",         row["verifyAccount"])
        saisir_champ(context.driver, "amount",                row["amount"])

        select = Select(context.driver.find_element(By.NAME, "fromAccountId"))
        select.select_by_index(0)
        time.sleep(DELAY)

        print(f"\n✅ Formulaire rempli : {row['payee']} | montant : {row['amount']}")

        context.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[value='Send Payment']")
        )).click()
        time.sleep(DELAY)
    except Exception as e:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/fill_form_FAILED.png")
        assert False, f"❌ FAILED : Remplissage formulaire échoué : {e}"


@when("il soumet le formulaire vide")
def step_submit_empty_form(context):
    try:
        context.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[value='Send Payment']")
        )).click()
        time.sleep(DELAY)
        print("\n✅ Formulaire vide soumis")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/submit_empty_FAILED.png")
        assert False, "❌ FAILED : Soumission formulaire vide échouée."


# ==========================
# THEN
# ==========================
@then('la confirmation de paiement doit s\'afficher avec "{payee}" et le montant "{amount}"')
def step_verify_confirmation(context, payee, amount):
    try:
        context.wait.until(EC.visibility_of_element_located((By.ID, "billpayResult")))
        time.sleep(DELAY)

        payee_name  = context.driver.find_element(By.ID, "payeeName").text
        paid_amount = context.driver.find_element(By.ID, "amount").text

        print(f"\n✅ Bénéficiaire : {payee_name} | Montant : {paid_amount}")
        assert payee in payee_name,   f"❌ Bénéficiaire inattendu : {payee_name}"
        assert amount in paid_amount, f"❌ Montant inattendu : {paid_amount}"
        print("\n✅ PASSED : Paiement confirmé !")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/confirmation_FAILED.png")
        assert False, "❌ FAILED : Confirmation de paiement introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()


@then("les erreurs de validation doivent s'afficher")
def step_verify_all_errors(context):
    try:
        time.sleep(DELAY)
        error_ids = [
            "validationModel-name",
            "validationModel-address",
            "validationModel-city",
            "validationModel-state",
            "validationModel-zipCode",
            "validationModel-phoneNumber",
            "validationModel-account-empty",
            "validationModel-verifyAccount-empty",
            "validationModel-amount-empty",
        ]
        visible_errors = []
        for error_id in error_ids:
            element = context.driver.find_element(By.ID, error_id)
            if element.is_displayed():
                visible_errors.append(element.text)
                print(f"  ❌ {element.text}")

        assert len(visible_errors) > 0, "❌ Aucune erreur affichée !"
        print(f"\n✅ PASSED : {len(visible_errors)} erreurs affichées !")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/validation_errors_FAILED.png")
        assert False, "❌ FAILED : Erreurs de validation introuvables."
    finally:
        time.sleep(2)
        context.driver.quit()


@then('l\'erreur "{expected_error}" doit s\'afficher')
def step_verify_specific_error(context, expected_error):
    try:
        time.sleep(DELAY)
        error_map = {
            "The amount cannot be empty.":       "validationModel-amount-empty",
            "Please enter a valid amount.":      "validationModel-amount-invalid",
            "The account numbers do not match.": "validationModel-verifyAccount-mismatch",
            "Please enter a valid number.":      "validationModel-account-invalid",
            "Account number is required.":       "validationModel-account-empty",
            "Payee name is required.":           "validationModel-name",
        }

        error_id = error_map.get(expected_error)
        if error_id:
            element = context.driver.find_element(By.ID, error_id)
            print(f"\n✅ Erreur : '{element.text}' | Visible : {element.is_displayed()}")
            assert element.is_displayed(), f"❌ Erreur non affichée : {expected_error}"
            print(f"\n✅ PASSED : Erreur correcte : {expected_error}")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/specific_error_FAILED.png")
        assert False, f"❌ FAILED : Erreur '{expected_error}' introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()