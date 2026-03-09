# features/request_loan.feature
@request_loan
Feature: Demande de prêt dans ParaBank
  En tant qu'utilisateur connecté à ParaBank
  Je veux tester les cas limites des montants et apports
  Afin de valider le comportement du système de demande de prêt

  Background:
    Given l'utilisateur est connecté à ParaBank pour la demande de prêt
    And l'utilisateur est sur la page "Request Loan"

  # ==========================
  # CAS VALIDES ✅
  # ==========================
  Scenario: Apport suffisant - prêt approuvé
    When il soumet une demande de prêt avec le montant "1000" et l'apport "99"
    Then le prêt doit être approuvé

  Scenario: Apport égal au montant - prêt approuvé
    When il soumet une demande de prêt avec le montant "1000" et l'apport "1000"
    Then le prêt doit être approuvé

  Scenario: Apport minimum accepté
    When il soumet une demande de prêt avec le montant "1000" et l'apport "1"
    Then le prêt doit être approuvé

  # ==========================
  # CAS LIMITES ⚠️
  # ==========================
  Scenario: Apport nul - prêt refusé
    When il soumet une demande de prêt avec le montant "1000" et l'apport "0"
    Then le prêt doit être refusé avec le message "You do not have sufficient funds for the given down payment."

  Scenario: Apport négatif - prêt refusé
    When il soumet une demande de prêt avec le montant "1000" et l'apport "-1"
    Then le prêt doit être refusé avec le message "You do not have sufficient funds for the given down payment."

  Scenario: Montant nul - prêt refusé
    When il soumet une demande de prêt avec le montant "0" et l'apport "99"
    Then le prêt doit être refusé avec le message "We cannot grant a loan in that amount with your available funds."

  Scenario: Montant négatif - prêt refusé
    When il soumet une demande de prêt avec le montant "-1000" et l'apport "99"
    Then le prêt doit être refusé avec le message "We cannot grant a loan in that amount with your available funds."

  Scenario: Montant très élevé - prêt refusé
    When il soumet une demande de prêt avec le montant "999999999" et l'apport "99"
    Then le prêt doit être refusé avec le message "We cannot grant a loan in that amount with your available funds and down payment."

  Scenario: Montant et apport nuls - prêt refusé
    When il soumet une demande de prêt avec le montant "0" et l'apport "0"
    Then le prêt doit être refusé avec le message "We cannot grant a loan in that amount with your available funds."

  # ==========================
  # CAS INVALIDES ❌
  # ==========================
  Scenario: Montant non numérique - erreur de validation
    When il soumet une demande de prêt avec le montant "abc" et l'apport "99"
    Then une erreur de validation doit s'afficher

  Scenario: Apport non numérique - erreur de validation
    When il soumet une demande de prêt avec le montant "1000" et l'apport "xyz"
    Then une erreur de validation doit s'afficher

  Scenario: Champs vides - erreur de validation
    When il soumet une demande de prêt avec le montant "vide" et l'apport "vide"
    Then une erreur de validation doit s'afficher