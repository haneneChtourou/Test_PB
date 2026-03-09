# features/find_transactions.feature

Feature: Recherche de transactions dans ParaBank
  En tant qu'utilisateur connecté à ParaBank pour Find Transactions
  Je veux rechercher des transactions selon différents critères
  Afin de retrouver facilement mes opérations bancaires

  Background:
    Given l'utilisateur est connecté à ParaBank pour Find Transactions
    And l'utilisateur est sur la page "Find Transactions"

  Scenario: Recherche de transaction par ID
    When il recherche une transaction avec l'ID "12145"
    Then la liste des transactions correspondantes doit s'afficher

  Scenario: Recherche de transactions par date
    When il recherche des transactions avec la date "04-03-2026"
    Then la liste des transactions correspondantes doit s'afficher

  Scenario: Recherche de transactions par plage de dates
    When il recherche des transactions entre "01-01-2024" et "31-12-2027"
    Then la liste des transactions correspondantes doit s'afficher

  Scenario: Recherche de transactions par montant
    When il recherche des transactions avec le montant "100"
    Then la liste des transactions correspondantes doit s'afficher
