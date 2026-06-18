provider "azurerm" {
  features {}
}

variable "location" {
  description = "Azure region used by exercise 1 resources."
  type        = string
  default     = "East US"
}

variable "resource_prefix" {
  description = "Prefix for exercise 1 resource names."
  type        = string
  default     = "exercicio1"
}

resource "random_id" "suffix" {
  byte_length = 4
}

locals {
  name_prefix    = lower(replace(var.resource_prefix, "_", "-"))
  name_suffix    = random_id.suffix.hex
  storage_prefix = lower(replace(var.resource_prefix, "/[^0-9a-z]/", ""))
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.name_prefix}-rg-${local.name_suffix}"
  location = var.location
}

resource "azurerm_storage_account" "sa" {
  name                     = substr("${local.storage_prefix}${local.name_suffix}", 0, 24)
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "sp" {
  name                = "${local.name_prefix}-sp-${local.name_suffix}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_cosmosdb_account" "cosmos" {
  name                = "${local.name_prefix}-cosmos-${local.name_suffix}"
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
  name                = "${local.name_prefix}-function-app-${local.name_suffix}"
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
    "CosmosDBConnection" = "AccountEndpoint=${azurerm_cosmosdb_account.cosmos.endpoint};AccountKey=${azurerm_cosmosdb_account.cosmos.primary_key};"
  }
}
