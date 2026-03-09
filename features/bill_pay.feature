# features/bill_pay.feature

Feature: Paiement de factures dans ParaBank
  En tant qu'utilisateur connecté à ParaBank
  Je veux payer des factures

  Background:
    Given l'utilisateur est connecté à ParaBank pour le paiement de factures
    And l'utilisateur est sur la page "Bill Pay"

  Scenario: Paiement valide avec confirmation
    When il remplit le formulaire avec les données suivantes
      | payee      | address     | city   | state | zipCode | phone        | account | verifyAccount | amount |
      | John Smith | 123 Main St | Boston | MA    | 02101   | 617-555-0100 | 12678   | 12678         | 100    |
    Then la confirmation de paiement doit s'afficher avec "John Smith" et le montant "$100.00"

  Scenario: Champs vides - erreurs de validation
    When il soumet le formulaire vide
    Then les erreurs de validation doivent s'afficher

  Scenario: Montant vide - erreur de validation
    When il remplit le formulaire avec les données suivantes
      | payee      | address     | city   | state | zipCode | phone        | account | verifyAccount | amount |
      | John Smith | 123 Main St | Boston | MA    | 02101   | 617-555-0100 | 12678   | 12678         |        |
    Then l'erreur "The amount cannot be empty." doit s'afficher

  Scenario: Numéros de compte non correspondants
    When il remplit le formulaire avec les données suivantes
      | payee      | address     | city   | state | zipCode | phone        | account | verifyAccount | amount |
      | John Smith | 123 Main St | Boston | MA    | 02101   | 617-555-0100 | 12678   | 99999         | 100    |
    Then l'erreur "The account numbers do not match." doit s'afficher

  Scenario: Compte invalide
    When il remplit le formulaire avec les données suivantes
      | payee      | address     | city   | state | zipCode | phone        | account | verifyAccount | amount |
      | John Smith | 123 Main St | Boston | MA    | 02101   | 617-555-0100 | abc     | abc           | 100    |
    Then l'erreur "Please enter a valid number." doit s'afficher