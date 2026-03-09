# features/open_account.feature

Feature: Création de compte dans ParaBank
  En tant qu'utilisateur connecté à ParaBank
  Je veux créer différents types de comptes
  Afin de gérer mes finances bancaires

  Background:
    Given l'utilisateur est connecté à ParaBank pour la création de compte
    And l'utilisateur est sur la page "Open New Account"

  # ==========================
  # CAS VALIDES ✅
  # ==========================
  Scenario: Créer un compte Checking
    When il sélectionne le type de compte "CHECKING"
    And il sélectionne le compte source
    And il clique sur "Open New Account"
    Then le nouveau compte Checking doit être créé avec succès
    And le numéro du nouveau compte doit être affiché

  Scenario: Créer un compte Savings
    When il sélectionne le type de compte "SAVINGS"
    And il sélectionne le compte source
    And il clique sur "Open New Account"
    Then le nouveau compte Savings doit être créé avec succès
    And le numéro du nouveau compte doit être affiché

  Scenario: Vérifier le solde initial du nouveau compte
    When il sélectionne le type de compte "CHECKING"
    And il sélectionne le compte source
    And il clique sur "Open New Account"
    Then le nouveau compte Checking doit être créé avec succès
    And le solde initial doit être supérieur à "100"

  # ==========================
  # CAS LIMITES ⚠️
  # ==========================
  Scenario: Créer un compte avec solde insuffisant
    When il sélectionne le type de compte "CHECKING"
    And il sélectionne un compte source avec solde insuffisant
    And il clique sur "Open New Account"
    Then une erreur de solde insuffisant doit s'afficher
