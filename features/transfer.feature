Feature: Transfer Funds ParaBank

  Scenario: Transfert valide entre deux comptes
    Given je suis connecté sur ParaBank
    And je vais sur Transfer Funds
    When je saisis le montant "50"
    And je clique sur Transfer
    Then je dois voir "Transfer Complete"

  Scenario: Transfert avec montant negatif
    Given je suis connecté sur ParaBank
    And je vais sur Transfer Funds
    When je saisis le montant "-100"
    And je clique sur Transfer
    Then je dois voir un message d'erreur transfert

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