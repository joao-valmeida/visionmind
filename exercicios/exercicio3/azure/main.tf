provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "exercicio3-rg"
  location = "East US"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "exercicio3-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "func_subnet" {
  name                 = "func-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
  delegation {
    name = "delegation"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_servicebus_namespace" "sb" {
  name                = "exercicio3-sb-ns"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"
}

resource "azurerm_servicebus_queue" "queue" {
  name         = "exercicio3-queue"
  namespace_id = azurerm_servicebus_namespace.sb.id
}

resource "azurerm_postgresql_flexible_server" "postgres" {
  name                   = "exercicio3-db-server"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "13"
  delegated_subnet_id    = null # Simplified for example
  administrator_login    = "psqladmin"
  administrator_password = "Password123!"
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2s_v3"
}

resource "azurerm_linux_function_app" "fa" {
  name                = "exercicio3-function-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = "ex3sa" # Needs to be unique
  storage_account_access_key = "..."
  service_plan_id            = "..."

  site_config {
    application_stack {
      python_version = "3.9"
    }
  }

  virtual_network_subnet_id = azurerm_subnet.func_subnet.id
}
