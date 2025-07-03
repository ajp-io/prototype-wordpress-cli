# WordPress Enterprise CLI Prototype

This repository contains a prototype implementation of the **Replicated Installer CLI** using WordPress Enterprise as an example application. This CLI demonstrates how enterprise software can be packaged and distributed with a user-friendly command-line interface for installation, configuration, and management.

## Overview

The WordPress Enterprise CLI prototype showcases the core functionality that would be available in a production Replicated Installer CLI:

- **Multi-platform deployment** (Kubernetes and Linux)
- **Airgap installation support** with air gap bundles
- **Certificate management** for secure access
- **Support bundle generation** for troubleshooting
- **Version management** and updates
- **Interactive configuration** wizards

## Features

### 🚀 Installation & Deployment
- **Kubernetes deployment**: Install WordPress Enterprise on Kubernetes clusters using Helm
- **Linux deployment**: Install directly on Linux hosts with k0s
- **Airgap support**: Install in offline environments using pre-packaged bundles
- **Certificate management**: Secure manager access with custom SSL certificates
- **Dry-run mode**: Preview installation commands without execution

### 🔧 Configuration & Management
- **Interactive setup**: Web-based configuration wizard integration
- **Password management**: Secure manager password setup
- **Multi-node clustering**: Join additional nodes to Linux clusters
- **High availability**: Enable HA mode for production deployments

### 🛠️ Operations & Support
- **Support bundles**: Generate diagnostic packages for troubleshooting
- **Shell access**: Access WordPress binaries directly (Linux only)
- **Uninstall**: Clean removal of WordPress Enterprise
- **Version updates**: CLI self-update functionality

## Installation

### Prerequisites
- Python 3.7+
- pip

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd wordpress_cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make the CLI executable and available as 'wordpress' command
chmod +x wordpress.py
ln -sf $(pwd)/wordpress.py /usr/local/bin/wordpress
```

## Usage

### Basic Installation

#### Kubernetes Deployment
```bash
# Install on Kubernetes with license
wordpress install --target kubernetes --license license.yaml

# Airgap installation with bundle
wordpress install --target kubernetes --license license.yaml --airgap-bundle wordpress.airgap

# Dry-run to preview commands
wordpress install --target kubernetes --license license.yaml --dry-run
```

#### Linux Deployment
```bash
# Basic Linux installation
wordpress install --target linux --license license.yaml

# With custom certificates
wordpress install --target linux --license license.yaml \
  --key-file /path/to/key.pem --cert-file /path/to/cert.pem

# Set custom manager port
wordpress install --target linux --license license.yaml --manager-port 30001
```

### Configuration

```bash
# Configure WordPress Enterprise settings
wordpress configure --license license.yaml
```

### Cluster Management

```bash
# Join a new node to Linux cluster
wordpress join --manager-password your-password

# Enable high availability
wordpress enable-ha
```

### Operations

```bash
# Generate support bundle
wordpress support-bundle

# Access WordPress shell (Linux only)
wordpress shell

# Uninstall WordPress Enterprise
wordpress uninstall
```

### Updates

```bash
# Update CLI to latest version
wordpress update

# Update to specific version
wordpress update --version 1.2.0

# Upgrade WordPress Enterprise
wordpress upgrade --target kubernetes --license license.yaml
```

## Configuration

The CLI uses a `config.yaml` file for prototype-specific settings:

```yaml
# Environment validation behavior
environment_validation: fail

# Sleep interval for operations (in seconds)
sleep_interval: 3

# Whether to push images to registry for online installations
push_images: true

# Whether to enable multi-node support for Linux installations
multi_node: true
```

## Command Reference

### `install`
Install WordPress Enterprise on the specified target platform.

**Options:**
- `--target`: Deployment target (`kubernetes` or `linux`)
- `--license`: Path to license file (required)
- `--airgap-bundle`: Path to airgap bundle file
- `--key-file`: Path to private key file for SSL
- `--cert-file`: Path to certificate file for SSL
- `--manager-port`: Port for WordPress Enterprise manager (default: 30000)
- `--manager-password`: Password for manager access
- `--dry-run`: Show commands without executing
- `--yes`: Answer yes to all prompts

### `upgrade`
Upgrade an existing WordPress Enterprise installation.

**Options:**
- `--target`: Deployment target (`kubernetes` or `linux`)
- `--license`: Path to license file (required for airgap)
- `--airgap-bundle`: Path to airgap bundle file
- `--key-file`: Path to private key file for SSL
- `--cert-file`: Path to certificate file for SSL
- `--dry-run`: Show commands without executing
- `--yes`: Answer yes to all prompts

### `configure`
Configure WordPress Enterprise settings via web interface.

**Options:**
- `--license`: Path to license file (required)

### `join`
Join a new node to a Linux cluster.

**Options:**
- `--manager-password`: Password for accessing the manager (required)

### `enable-ha`
Enable high availability mode on Linux cluster.

### `shell`
Start a shell with WordPress binaries in PATH (Linux only).

### `support-bundle`
Generate a support bundle for troubleshooting.

### `uninstall`
Remove WordPress Enterprise from the current node.

### `update`
Update the CLI to the latest version.

**Options:**
- `--version`: Specific version to update to
- `--yes`: Answer yes to all prompts

## File Structure

```
wordpress_cli/
├── wordpress.py          # Main CLI application
├── requirements.txt      # Python dependencies
├── config.yaml           # Prototype configuration
├── config-values.yaml    # Generated configuration values
├── license.yaml          # Example license file
├── wordpress.airgap      # Example airgap bundle
├── wordpress.tgz         # Generated Helm chart
├── wordpress.yaml        # Generated values file
└── README.md             # This file
```

## Dependencies

- **click**: Command-line interface creation kit
- **halo**: Terminal spinners for better UX
- **colorama**: Cross-platform colored terminal text
- **PyYAML**: YAML parser and emitter
- **packaging**: Core utilities for Python packages

## Development

This is a prototype implementation that simulates the behavior of a production Replicated Installer CLI. The actual installation, upgrade, and configuration processes are simulated with delays and spinners to demonstrate the user experience.

### Key Prototype Features:
- **Simulated operations**: All long-running operations use configurable delays
- **Interactive prompts**: Password confirmation, certificate warnings, etc.
- **File generation**: Creates example files (Helm charts, configs, bundles)
- **Progress indicators**: Uses spinners to show operation progress
- **Error handling**: Demonstrates proper error states and validation

## License

This prototype is for demonstration purposes only. The actual Replicated Installer CLI would be subject to its own licensing terms.

## Contributing

This is a prototype repository for demonstrating CLI functionality. For production use, refer to the official Replicated documentation and tools. 