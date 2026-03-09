from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from environment import creer_driver, BASE_URL
import os
import time


@given("l'utilisateur est connecté à ParaBank pour Find Transactions")
def step_login_find_transactions(context):
    context.driver = creer_driver()
    context.wait   = WebDriverWait(context.driver, 15)

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
    context.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Welcome')]")))
    print(f"\n▶️  Connecté ! Démarrage : {context.scenario.name}")


@given('l\'utilisateur est sur la page "Find Transactions"')
def step_open_find_transactions(context):
    try:
        context.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Find Transactions")
        )).click()

        context.wait.until(EC.visibility_of_element_located((By.ID, "accountId")))

        select = Select(context.driver.find_element(By.ID, "accountId"))
        select.select_by_index(0)
        print(f"\n✅ Compte sélectionné : {select.first_selected_option.text}")
        print("\n✅ Page Find Transactions ouverte")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/find_transactions_FAILED.png")
        assert False, "❌ FAILED : Page Find Transactions introuvable."


@when('il recherche une transaction avec l\'ID "{transaction_id}"')
def step_search_by_id(context, transaction_id):
    try:
        if os.path.exists("transaction_id.txt"):
            with open("transaction_id.txt", "r") as f:
                transaction_id = f.read().strip()
            print(f"\n✅ ID récupéré depuis fichier : {transaction_id}")
        else:
            print(f"\n⚠️ Fichier introuvable, utilise ID : {transaction_id}")

        id_input = context.wait.until(
            EC.visibility_of_element_located((By.ID, "transactionId"))
        )
        id_input.clear()
        id_input.send_keys(transaction_id)
        time.sleep(1)
        print(f"\n✅ ID saisi : '{transaction_id}'")

        context.wait.until(EC.element_to_be_clickable((By.ID, "findById"))).click()
        context.wait.until(EC.visibility_of_element_located((By.ID, "resultContainer")))
        print(f"\n✅ Recherche effectuée par ID : {transaction_id}")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/search_id_FAILED.png")
        assert False, f"❌ FAILED : Recherche par ID '{transaction_id}' échouée."


@when('il recherche des transactions avec la date "{date}"')
def step_search_by_date(context, date):
    try:
        date_input = context.wait.until(
            EC.visibility_of_element_located((By.ID, "transactionDate"))
        )
        date_input.clear()
        date_input.send_keys(date)
        time.sleep(1)
        print(f"\n✅ Date saisie : '{date}'")

        context.wait.until(EC.element_to_be_clickable((By.ID, "findByDate"))).click()
        context.wait.until(EC.visibility_of_element_located((By.ID, "resultContainer")))
        print(f"\n✅ Recherche effectuée par date : {date}")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/search_date_FAILED.png")
        assert False, f"❌ FAILED : Recherche par date '{date}' échouée."


@when('il recherche des transactions entre "{from_date}" et "{to_date}"')
def step_search_by_date_range(context, from_date, to_date):
    try:
        from_input = context.wait.until(
            EC.visibility_of_element_located((By.ID, "fromDate"))
        )
        from_input.clear()
        from_input.send_keys(from_date)

        to_input = context.wait.until(
            EC.visibility_of_element_located((By.ID, "toDate"))
        )
        to_input.clear()
        to_input.send_keys(to_date)
        time.sleep(1)
        print(f"\n✅ Plage saisie : '{from_date}' → '{to_date}'")

        context.wait.until(EC.element_to_be_clickable((By.ID, "findByDateRange"))).click()
        context.wait.until(EC.visibility_of_element_located((By.ID, "resultContainer")))
        print(f"\n✅ Recherche effectuée par plage : {from_date} → {to_date}")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/search_date_range_FAILED.png")
        assert False, f"❌ FAILED : Recherche par plage '{from_date}' → '{to_date}' échouée."


@when('il recherche des transactions avec le montant "{montant}"')
def step_search_by_amount(context, montant):
    try:
        amount_input = context.wait.until(
            EC.visibility_of_element_located((By.ID, "amount"))
        )
        amount_input.clear()
        amount_input.send_keys(montant)
        time.sleep(1)
        print(f"\n✅ Montant saisi : '{montant}'")

        context.wait.until(EC.element_to_be_clickable((By.ID, "findByAmount"))).click()
        context.wait.until(EC.visibility_of_element_located((By.ID, "resultContainer")))
        print(f"\n✅ Recherche effectuée par montant : {montant}")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/search_amount_FAILED.png")
        assert False, f"❌ FAILED : Recherche par montant '{montant}' échouée."


@then("la liste des transactions correspondantes doit s'afficher")
def step_verify_results(context):
    try:
        context.wait.until(
            EC.visibility_of_element_located((By.ID, "transactionTable"))
        )

        rows = context.driver.find_elements(
            By.XPATH, "//tbody[@id='transactionBody']/tr"
        )

        print(f"\n✅ Nombre de transactions trouvées : {len(rows)}")
        for i, row in enumerate(rows):
            print(f"  Transaction {i+1} : {row.text}")

        assert len(rows) > 0, "❌ Aucune transaction trouvée !"
        print("\n✅ PASSED : Transactions affichées avec succès !")
    except AssertionError:
        raise
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/find_results_FAILED.png")
        assert False, "❌ FAILED : Liste des transactions introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()