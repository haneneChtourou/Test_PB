Feature: Connexion ParaBank

  Background:
    Given j'ouvre ParaBank

  Scenario: Connexion avec identifiants valides
    When je saisis username "john" et password "demo"
    And je clique sur Log In
    Then je dois voir "Welcome"

  Scenario: Connexion avec username inexistant
    When je saisis username "user_inexistant_999" et password "demo"
    And je clique sur Log In
    Then je dois voir un message d'erreur

  Scenario: Connexion avec mot de passe incorrect
    When je saisis username "john" et password "mauvais_mdp"
    And je clique sur Log In
    Then je dois voir un message d'erreur