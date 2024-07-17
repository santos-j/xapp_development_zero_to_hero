# Commands for managing xApps on a Near-RT RIC


## Onboard xApps

```bash
# Onboard xApp to generate its chart
dms_cli onboard <CONFIG_JSON> <SCHEMA_JSON>

# Or
dms_cli onboard --config_file_path=<CONFIG_JSON> --schema_file_path=<SCHEMA_JSON>
```

```bash
# Example of an onboarding command
dms_cli onboard xapp_path/init/config_file.json xapp_path/init/schema_file.json
```

## Installing xApps

```bash
# Install an xApp on the Near-RT RIC
dms_cli install <XAPP_CHART_NAME> <VERSION> <NAMESPACE>

# Or
dms_cli install --xapp_chart_name=<XAPP_CHART_NAME> --version=<VERSION> --namespace=<NAMESPACE>
```

```bash
# Example of an install command
dms_cli install example_xapp 1.0.0 ricxapp
```

## Uninstalling xApps

```bash
# Uninstall an xApp from the Near-RT RIC
dms_cli uninstall <XAPP_CHART_NAME> <NAMESPACE>

# Or
dms_cli uninstall --xapp_chart_name=<XAPP_CHART_NAME> --namespace=<NAMESPACE>
```

```bash
# Example of an uninstall command
dms_cli uninstall example_xapp ricxap
```

## Upgrading xApps

```bash
# Upgrade an xApp to a new version
dms_cli upgrade --xapp_chart_name=<XAPP_CHART_NAME> --old_version=<OLD_VERSION> --new_version=<NEW_VERSION> --namespace=<NAMESPACE>
```

```bash
# Example of an upgrade command
dms_cli upgrade --xapp_chart_name=example_xapp --old_version=1.0.0 --new_version=1.1.0 --namespace=ricxapp
```

## Rolling Back xApps

```bash
# Roll back an xApp to a previous version
dms_cli rollback --xapp_chart_name=<XAPPI_CHART_NAME> --new_version=<NEW_VERSION> --old_version=<OLD_VERSION> --namespace=<NAMESPACE>
```

```bash
# Example of a rollback command
dms_cli rollback --xapp_chart_name=example_xapp ---old_version=1.1.0 --new_version=1.0.0 --namespace=ricxapp
```

## Check the status of the Helm Chart Repository

```bash
# Check health of Helm Chart Repository
dms_cli health
```

## Check the list of onboarded xApps

```bash
# Query list of onboarded xApps
dms_cli get_charts_list
```

## Check the heatlh of a running xApp pod

```bash
# Check the health of an xApp pod
dms_cli health_check --xapp_chart_name=<XAPP_CHART_NAME> --namespace=<NAMESPACE>
```

## Download the xApp Helm Chart

```bash
# Download the xApp Helm Charts
dms_cli download_values_yaml --xapp_chart_name=<XAPP_NAME> --version=<VERSION> --output_path=<OUTPUT_PATH>
```

## Override the xApp Helm Chart

```bash
# Override xApp Helm Chart's values.yaml
dms_cli install <XAPP_CHART_NAME> <VERSION> <NAMESPACE> --overridefile <VALUES_PATH>
```
