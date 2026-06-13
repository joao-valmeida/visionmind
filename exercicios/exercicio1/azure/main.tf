provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "exercicio1-rg"
  location = "East US"
}

resource "azurerm_storage_account" "sa" {
  name                     = "exercicio1sa"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "sp" {
  name                = "exercicio1-sp"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_cosmosdb_account" "cosmos" {
  name                = "exercicio1-cosmos"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }
}

resource "azurerm_linux_function_app" "fa" {
  name                = "exercicio1-function-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = azurerm_storage_account.sa.name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key
  service_plan_id            = azurerm_service_plan.sp.id

  site_config {
    application_stack {
      python_version = "3.9"
    }
  }

  app_settings = {
    "CosmosDBConnection" = azurerm_cosmosdb_account.cosmos.connection_strings[0]
  }
}
