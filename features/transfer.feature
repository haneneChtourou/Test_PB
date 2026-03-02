Feature: Transfer Funds ParaBank

  Scenario: Transfert valide entre deux comptes
    Given je suis connecté sur ParaBank
    And je vais sur Transfer Funds
    When je saisis le montant "50"
    And je clique sur Transfer
    Then je dois voir "Transfer Complete"

  Scenario: Transfert avec montant negatif - BUG ATTENDU
    Given je suis connecté sur ParaBank
    And je vais sur Transfer Funds
    When je saisis le montant "-100"
    And je clique sur Transfer
    Then le transfert negatif doit etre refuse

  Scenario: Transfert avec montant vide
    Given je suis connecté sur ParaBank
    And je vais sur Transfer Funds
    When je laisse le montant vide
    And je clique sur Transfer
    Then je dois voir un message d'erreur transfert

  Scenario: Transfert avec caractere non numerique
    Given je suis connecté sur ParaBank
    And je vais sur Transfer Funds
    When je saisis le montant "abc"
    And je clique sur Transfer
    Then je dois voir un message d'erreur transfert

  Scenario: CAS 14 - Vérifier les détails d'une transaction après transfert
    Given je suis connecté sur ParaBank
    And je vais sur Transfer Funds
    When je saisis le montant "100"
    And je clique sur Transfer
    Then je dois voir "Transfer Complete"
    When je vais sur Accounts Overview
    And je clique sur le compte source
    Then je dois voir Account Activity
    And la transaction de "-$100.00" doit apparaitre dans la liste
    When je clique sur Funds Transfer Sent
    Then je dois voir Transaction Details