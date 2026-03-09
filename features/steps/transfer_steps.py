
# from behave import given, when, then
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
# from environment import creer_driver
# import os
# import time


# @given("je suis connecté sur ParaBank")
# def step_login(context):
#     context.driver = creer_driver()
#     context.wait   = WebDriverWait(context.driver, 15)

#     context.driver.get("about:blank")
#     context.driver.get("https://parabank.parasoft.com")
#     context.driver.delete_all_cookies()
#     context.driver.execute_script("window.localStorage.clear();")
#     context.driver.execute_script("window.sessionStorage.clear();")
#     context.driver.get("https://parabank.parasoft.com/parabank/index.htm")
#     context.wait.until(EC.presence_of_element_located((By.NAME, "username")))

#     field_user = context.driver.find_element(By.NAME, "username")
#     field_user.clear()
#     field_user.send_keys("john")

#     field_pass = context.driver.find_element(By.NAME, "password")
#     field_pass.clear()
#     field_pass.send_keys("demo")

#     context.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Log In']"))).click()
#     context.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Welcome')]")))
#     print(f"\n▶️  Démarrage : {context.scenario.name}")


# @given("je vais sur Transfer Funds")
# def step_go_transfer(context):
#     context.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))).click()
#     field = context.wait.until(EC.element_to_be_clickable((By.ID, "amount")))
#     field.click()
#     print("\n✅ Page Transfer Funds chargée !")

#     context.wait.until(lambda d: len(Select(d.find_element(By.ID, "fromAccountId")).options) > 0)
#     from_select = Select(context.driver.find_element(By.ID, "fromAccountId"))
#     from_select.select_by_index(0)
#     context.compte_source = from_select.options[0].text.strip()
#     print(f"\n✅ From compte : {context.compte_source}")

#     context.wait.until(lambda d: len(Select(d.find_element(By.ID, "toAccountId")).options) > 1)
#     to_select = Select(context.driver.find_element(By.ID, "toAccountId"))
#     to_select.select_by_index(1)
#     print(f"\n✅ To compte : {to_select.options[1].text.strip()}")


# @when('je saisis le montant "{montant}"')
# def step_amount(context, montant):
#     field = context.wait.until(EC.element_to_be_clickable((By.ID, "amount")))
#     field.click()
#     field.clear()
#     field.send_keys(montant)
#     print(f"\n✅ Montant saisi : '{montant}'")


# @when("je laisse le montant vide")
# def step_amount_vide(context):
#     field = context.wait.until(EC.element_to_be_clickable((By.ID, "amount")))
#     field.click()
#     field.clear()
#     print("\n✅ Montant laissé vide")


# @when("je clique sur Transfer")
# def step_click_transfer(context):
#     context.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Transfer']"))).click()


# @then('je dois voir "Transfer Complete"')
# def step_transfer_success(context):
#     try:
#         context.wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//*[contains(text(),'Transfer Complete')]")
#         ))
#         print("\n✅ PASSED : TRANSFERT REUSSI !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         context.driver.save_screenshot("screenshots/transfer_valide_FAILED.png")
#         assert False, "❌ FAILED : 'Transfer Complete' introuvable."
#     finally:
#         if "CAS 14" not in context.scenario.name:
#             time.sleep(2)
#             context.driver.quit()


# @then("le transfert negatif doit etre refuse")
# def step_transfer_negatif_bug(context):
#     try:
#         element = context.driver.find_element(
#             By.XPATH, "//*[contains(text(),'Transfer Complete')]"
#         )
#         if element:
#             print("\n❌ BUG DETECTE : ParaBank accepte les montants négatifs !")
#             os.makedirs("screenshots", exist_ok=True)
#             context.driver.save_screenshot("screenshots/bug_montant_negatif.png")
#             assert False, "❌ BUG : Montant négatif accepté, message d'erreur attendu."
#     except AssertionError:
#         raise
#     except Exception:
#         print("\n✅ PASSED : Montant négatif refusé correctement !")
#     finally:
#         time.sleep(2)
#         context.driver.quit()


# @then("je dois voir un message d'erreur transfert")
# def step_transfer_error(context):
#     try:
#         context.wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//*[contains(text(),'Error') or contains(text(),'error') or contains(text(),'Please')]")
#         ))
#         print("\n✅ PASSED : MESSAGE D'ERREUR TRANSFERT PRESENT !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         nom = context.scenario.name.replace(" ", "_")
#         context.driver.save_screenshot(f"screenshots/{nom}_FAILED.png")
#         assert False, "❌ FAILED : Message d'erreur transfert introuvable."
#     finally:
#         time.sleep(2)
#         context.driver.quit()


# # ══════════════════════════════════════════════════════
# #  CAS 14 - DETAILS DE TRANSACTION
# # ══════════════════════════════════════════════════════

# @when("je vais sur Accounts Overview")
# def step_go_accounts_overview(context):
#     try:
#         context.wait.until(EC.element_to_be_clickable(
#             (By.LINK_TEXT, "Accounts Overview")
#         )).click()
#         context.wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//*[contains(text(),'Accounts Overview')]")
#         ))
#         print("\n✅ Page Accounts Overview chargée !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         assert False, "❌ FAILED : Page Accounts Overview introuvable."


# @when("je clique sur le compte source")
# def step_click_compte_source(context):
#     try:
#         lien_compte = context.wait.until(EC.element_to_be_clickable(
#             (By.XPATH, f"//a[contains(text(),'{context.compte_source}')]")
#         ))
#         lien_compte.click()
#         context.wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//*[contains(text(),'Account Details')]")
#         ))
#         print(f"\n✅ Page du compte {context.compte_source} chargée !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         assert False, f"❌ FAILED : Compte source {context.compte_source} introuvable."


# @then("je dois voir Account Activity")
# def step_check_account_activity(context):
#     try:
#         context.wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//*[contains(text(),'Account Activity')]")
#         ))
#         print("\n✅ PASSED : Section Account Activity présente !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         assert False, "❌ FAILED : Account Activity introuvable."


# @then('la transaction de "{montant}" doit apparaitre dans la liste')
# def step_check_transaction_in_list(context, montant):
#     try:
#         context.wait.until(EC.presence_of_element_located(
#             (By.XPATH, f"//table[@id='transactionTable']//*[contains(text(),'{montant}')]")
#         ))
#         print(f"\n✅ PASSED : Transaction {montant} présente dans la liste !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         nom = context.scenario.name.replace(" ", "_")
#         context.driver.save_screenshot(f"screenshots/{nom}_FAILED.png")
#         assert False, f"❌ FAILED : Transaction {montant} introuvable dans la liste."


# @when("je clique sur Funds Transfer Sent")
# def step_click_funds_transfer_sent(context):
#     try:
#         from datetime import datetime
#         # Date d'aujourd'hui format MM-DD-YYYY (format ParaBank)
#         today = datetime.now().strftime("%m-%d-%Y")
#         print(f"\n✅ Date recherchée : {today}")

#         # Cherche la ligne avec la date d'aujourd'hui ET 100.00
#         # Clique sur le lien dans la 2ème colonne (Funds Transfer Sent)
#         lien = context.wait.until(EC.element_to_be_clickable(
#             (By.XPATH, f"//table[@id='transactionTable']//tr[contains(., '{today}') and contains(., '100.00')]//td[2]//a")
#         ))
#         print(f"\n✅ Transaction trouvée : {lien.text}")
#         lien.click()
#         context.wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//*[contains(text(),'Transaction Details')]")
#         ))
#         print("\n✅ Page Transaction Details chargée !")
#     except Exception as e:
#         print(f"\n❌ Erreur : {e}")
#         os.makedirs("screenshots", exist_ok=True)
#         context.driver.save_screenshot("screenshots/funds_transfer_sent_FAILED.png")
#         assert False, "❌ FAILED : Transaction Funds Transfer Sent introuvable."


# @then("je dois voir Transaction Details")
# def step_check_transaction_details(context):
#     try:
#         context.wait.until(EC.presence_of_element_located(
#             (By.XPATH, "//*[contains(text(),'Transaction Details')]")
#         ))
#         print("\n✅ PASSED : Transaction Details affichée !")
#     except Exception:
#         os.makedirs("screenshots", exist_ok=True)
#         context.driver.save_screenshot("screenshots/transaction_details_FAILED.png")
#         assert False, "❌ FAILED : Transaction Details introuvable."
#     finally:
#         time.sleep(2)
#         context.driver.quit()


from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from environment import creer_driver, BASE_URL
import os
import time


@given("je suis connecté sur ParaBank")
def step_login(context):
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
    print(f"\n▶️  Démarrage : {context.scenario.name}")


@given("je vais sur Transfer Funds")
def step_go_transfer(context):
    context.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))).click()
    field = context.wait.until(EC.element_to_be_clickable((By.ID, "amount")))
    field.click()
    print("\n✅ Page Transfer Funds chargée !")

    context.wait.until(lambda d: len(Select(d.find_element(By.ID, "fromAccountId")).options) > 0)
    from_select = Select(context.driver.find_element(By.ID, "fromAccountId"))
    from_select.select_by_index(0)
    context.compte_source = from_select.options[0].text.strip()
    print(f"\n✅ From compte : {context.compte_source}")

    context.wait.until(lambda d: len(Select(d.find_element(By.ID, "toAccountId")).options) > 1)
    to_select = Select(context.driver.find_element(By.ID, "toAccountId"))
    to_select.select_by_index(1)
    print(f"\n✅ To compte : {to_select.options[1].text.strip()}")


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
        context.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Transfer Complete')]")
        ))
        print("\n✅ PASSED : TRANSFERT REUSSI !")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/transfer_valide_FAILED.png")
        assert False, "❌ FAILED : 'Transfer Complete' introuvable."
    finally:
        if "CAS 14" not in context.scenario.name:
            time.sleep(2)
            context.driver.quit()


@then("le transfert negatif doit etre refuse")
def step_transfer_negatif_bug(context):
    try:
        element = context.driver.find_element(
            By.XPATH, "//*[contains(text(),'Transfer Complete')]"
        )
        if element:
            print("\n❌ BUG DETECTE : ParaBank accepte les montants négatifs !")
            os.makedirs("screenshots", exist_ok=True)
            context.driver.save_screenshot("screenshots/bug_montant_negatif.png")
            assert False, "❌ BUG : Montant négatif accepté, message d'erreur attendu."
    except AssertionError:
        raise
    except Exception:
        print("\n✅ PASSED : Montant négatif refusé correctement !")
    finally:
        time.sleep(2)
        context.driver.quit()


@then("je dois voir un message d'erreur transfert")
def step_transfer_error(context):
    try:
        context.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Error') or contains(text(),'error') or contains(text(),'Please')]")
        ))
        print("\n✅ PASSED : MESSAGE D'ERREUR TRANSFERT PRESENT !")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        nom = context.scenario.name.replace(" ", "_")
        context.driver.save_screenshot(f"screenshots/{nom}_FAILED.png")
        assert False, "❌ FAILED : Message d'erreur transfert introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()


# ══════════════════════════════════════════════════════
#  CAS 14 - DETAILS DE TRANSACTION
# ══════════════════════════════════════════════════════

@when("je vais sur Accounts Overview")
def step_go_accounts_overview(context):
    try:
        context.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, "Accounts Overview")
        )).click()
        context.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Accounts Overview')]")
        ))
        print("\n✅ Page Accounts Overview chargée !")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        assert False, "❌ FAILED : Page Accounts Overview introuvable."


@when("je clique sur le compte source")
def step_click_compte_source(context):
    try:
        lien_compte = context.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//a[contains(text(),'{context.compte_source}')]")
        ))
        lien_compte.click()
        context.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Account Details')]")
        ))
        print(f"\n✅ Page du compte {context.compte_source} chargée !")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        assert False, f"❌ FAILED : Compte source {context.compte_source} introuvable."


@then("je dois voir Account Activity")
def step_check_account_activity(context):
    try:
        context.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Account Activity')]")
        ))
        print("\n✅ PASSED : Section Account Activity présente !")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        assert False, "❌ FAILED : Account Activity introuvable."


@then('la transaction de "{montant}" doit apparaitre dans la liste')
def step_check_transaction_in_list(context, montant):
    try:
        context.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//table[@id='transactionTable']//*[contains(text(),'{montant}')]")
        ))
        print(f"\n✅ PASSED : Transaction {montant} présente dans la liste !")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        nom = context.scenario.name.replace(" ", "_")
        context.driver.save_screenshot(f"screenshots/{nom}_FAILED.png")
        assert False, f"❌ FAILED : Transaction {montant} introuvable dans la liste."


@when("je clique sur Funds Transfer Sent")
def step_click_funds_transfer_sent(context):
    try:
        from datetime import datetime
        context.today = datetime.now().strftime("%m-%d-%Y")

        lien = context.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//table[@id='transactionTable']//tr[contains(., '{context.today}') and contains(., '100.00')]//td[2]//a")
        ))
        print(f"\n✅ Transaction trouvée : {lien.text}")
        lien.click()
        context.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Transaction Details')]")
        ))
        print("\n✅ Page Transaction Details chargée !")

        # Récupère l'ID depuis l'URL
        url = context.driver.current_url
        transaction_id = url.split("id=")[-1]
        context.transaction_id = transaction_id
        print(f"\n✅ ID Transaction récupéré : {transaction_id}")

        # Sauvegarde dans un fichier
        with open("transaction_id.txt", "w") as f:
            f.write(transaction_id)
        print(f"\n✅ ID sauvegardé dans transaction_id.txt")

    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/funds_transfer_sent_FAILED.png")
        assert False, "❌ FAILED : Lien 'Funds Transfer Sent' introuvable."


@then("je dois voir Transaction Details")
def step_check_transaction_details(context):
    try:
        context.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Transaction Details')]")
        ))
        print("\n✅ PASSED : Transaction Details affichée !")
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        context.driver.save_screenshot("screenshots/transaction_details_FAILED.png")
        assert False, "❌ FAILED : Transaction Details introuvable."
    finally:
        time.sleep(2)
        context.driver.quit()