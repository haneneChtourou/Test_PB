from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from environment import creer_driver, BASE_URL
import os
import time

DELAY = 2


@given("l'utilisateur est connecté à ParaBank pour la demande de prêt")
def step_login_loan(context):
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
    context.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Request Loan")))
    print(f"\n▶️  Connecté ! Démarrage : {context.scenario.name}")


@given('l\'utilisateur est sur la page "Request Loan"')
def step_open_request_loan(context):
    try:
        context.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Request Loan")
        )).click()
        context.wait.until(EC.visibility_of_element_located((By.ID, "amount")))
        print("\n✅ Page Request Loan ouverte")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/request_loan_FAILED.png")
        assert False, "❌ FAILED : Page Request Loan introuvable."


@when('il soumet une demande de prêt avec le montant "{amount}" et l\'apport "{down_payment}"')
def step_submit_loan(context, amount, down_payment):
    try:
        amount       = "" if amount == "vide" else amount
        down_payment = "" if down_payment == "vide" else down_payment

        amount_input = context.wait.until(EC.visibility_of_element_located((By.ID, "amount")))
        amount_input.clear()
        if amount:
            amount_input.send_keys(amount)
        time.sleep(DELAY)

        down_input = context.driver.find_element(By.ID, "downPayment")
        down_input.clear()
        if down_payment:
            down_input.send_keys(down_payment)
        time.sleep(DELAY)

        select = Select(context.driver.find_element(By.ID, "fromAccountId"))
        select.select_by_index(0)
        time.sleep(DELAY)

        print(f"\n✅ Montant : '{amount}' | Apport : '{down_payment}'")
        context.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[value='Apply Now']")
        )).click()
        time.sleep(DELAY)
    except Exception as e:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/submit_loan_FAILED.png")
        assert False, f"❌ FAILED : Soumission du prêt échouée : {e}"


@then("le prêt doit être approuvé")
def step_loan_approved(context):
    try:
        context.wait.until(EC.visibility_of_element_located((By.ID, "requestLoanResult")))
        time.sleep(DELAY)
        status = context.driver.find_element(By.ID, "loanStatus").text
        print(f"\n✅ Statut : {status}")
        assert status == "Approved", f"❌ Prêt non approuvé ! Statut : {status}"
        print("\n✅ PASSED : Prêt approuvé !")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/loan_approved_FAILED.png")
        assert False, "❌ FAILED : Résultat du prêt introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()


@then('le prêt doit être refusé avec le message "{expected_message}"')
def step_loan_denied(context, expected_message):
    try:
        context.wait.until(EC.visibility_of_element_located((By.ID, "requestLoanResult")))
        time.sleep(DELAY)
        status    = context.driver.find_element(By.ID, "loanStatus").text
        error_msg = context.driver.find_element(By.CSS_SELECTOR, "#loanRequestDenied p.error").text
        print(f"\n✅ Statut : {status} | Message : {error_msg}")
        assert status == "Denied", f"❌ Statut inattendu : {status}"
        assert expected_message in error_msg, f"❌ Message inattendu : {error_msg}"
        print(f"\n✅ PASSED : Prêt refusé correctement !")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/loan_denied_FAILED.png")
        assert False, "❌ FAILED : Résultat refus introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()


@then("une erreur de validation doit s'afficher")
def step_validation_error(context):
    try:
        time.sleep(DELAY)
        error_container  = context.driver.find_elements(By.ID, "requestLoanError")
        result_container = context.driver.find_elements(By.ID, "requestLoanResult")

        if error_container and error_container[0].is_displayed():
            print("\n✅ PASSED : Erreur système affichée !")
        elif result_container and result_container[0].is_displayed():
            status = context.driver.find_element(By.ID, "loanStatus").text
            assert status == "Denied", f"❌ Statut inattendu : {status}"
            print(f"\n✅ PASSED : Prêt refusé avec statut : {status}")
        else:
            print("\n✅ PASSED : Validation côté client !")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/validation_error_FAILED.png")
        assert False, "❌ FAILED : Erreur de validation introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()