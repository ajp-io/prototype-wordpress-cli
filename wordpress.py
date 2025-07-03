#!/usr/bin/env python3

import click
from halo import Halo
import time
import signal
import os
import yaml
from packaging import version as packaging_version

# Current version of the CLI
CURRENT_VERSION = "1.0.0"

def check_for_updates():
    """Check if a new version is available"""
    try:
        # In a real implementation, this would check against a version API
        # For the prototype, we'll simulate a newer version being available
        latest_version = "1.1.0"
        if packaging_version.parse(latest_version) > packaging_version.parse(CURRENT_VERSION):
            return latest_version
    except Exception:
        # If we can't check for updates, continue without showing the message
        pass
    return None

CONFIG_PATH = os.path.join(os.getcwd(), 'config.yaml')

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    return {}

@click.group()
def cli():
    """WordPress Enterprise Installer"""
    pass

# INSTALL COMMAND
@cli.command()
@click.option('--airgap-bundle', type=click.Path(exists=True), help='Path to airgap bundle file')
@click.option('--cert-file', type=click.Path(exists=True), help='Path to certificate file for securing WordPress Enterprise manager access')
@click.option('--dry-run', is_flag=True, help='Show the install commands instead of executing them')
@click.option('--manager-password', help='Set password for accessing the WordPress Enterprise manager')
@click.option('--manager-port', type=int, default=30000, help='Port on which the WordPress Enterprise manager will be accessed')
@click.option('--key-file', type=click.Path(exists=True), help='Path to private key file for securing WordPress Enterprise manager access')
@click.option('--license', '-l', 'license_path', type=click.Path(exists=True), required=True, help='Path to a license file')
@click.option('--target', type=click.Choice(['kubernetes', 'linux']), required=True, help='Deployment target')
@click.option('-y', '--yes', is_flag=True, help='Answer yes to all prompts')
def install(dry_run, airgap_bundle, license_path, key_file, cert_file, manager_port, manager_password, target, yes):
    """Install WordPress Enterprise"""
    config = load_config()
    
    # Check if certificate files are provided (only for Linux installations)
    if target == 'linux' and not (key_file and cert_file):
        click.echo(click.style("No certificate files provided. A self-signed certificate will be used.", fg='yellow'))
        click.echo("To use your own certificate, provide both --key-file and --cert-file flags.\n")
        if not yes and not click.confirm("Do you want to continue with a self-signed certificate?", default=False):
            click.echo("\nInstallation cancelled. Please run the command again with --key-file and --cert-file flags.\n")
            return
    
    # Get manager password if not provided
    if not manager_password:
        attempts = 0
        while attempts < 3:
            manager_password = click.prompt("\nSet password for WordPress Enterprise manager", hide_input=True)
            confirm = click.prompt("Confirm password", hide_input=True)
            if manager_password == confirm:
                break
            attempts += 1
            if attempts < 3:
                click.echo("Passwords do not match. Please try again.")
            else:
                click.echo("\nToo many failed attempts. Installation cancelled.\n")
                return
    
    click.echo("\nVisit the WordPress Enterprise manager to continue:")
    click.echo(f"https://shorturl.at/c21df:{manager_port}")
    time.sleep(config.get('sleep_interval', 3))
    click.echo("")
    wait_text = 'Waiting for configuration'
    wait_spinner = Halo(text=f'{wait_text}', spinner='dots')
    wait_spinner.start()
    time.sleep(config.get('sleep_interval', 3))
    wait_spinner.succeed('Configuration complete')

    if target == 'kubernetes':
        if dry_run:
            file_spinner = Halo(text='Preparing files', spinner='dots')
            file_spinner.start()
            with open('wordpress.tgz', 'wb') as f:
                f.write(b'')
            with open('wordpress.yaml', 'w') as f:
                f.write('# values.yaml for wordpress\n')
            time.sleep(config.get('sleep_interval', 3))
            file_spinner.succeed('Files prepared')
            click.echo("\nUse the following docker commands to load and push the images:")
            if airgap_bundle:
                click.echo(f"docker load -i {airgap_bundle}")
            else:
                click.echo("docker pull images.wordpress.com/proxy/wordpress/wordpress:latest")
                click.echo("docker pull images.wordpress.com/proxy/wordpress/wordpress-runner:latest")
                click.echo("docker pull images.wordpress.com/proxy/wordpress/wordpress-actions-runner:latest")
            click.echo("docker tag wordpress:latest registry.example.com/wordpress:latest")
            click.echo("docker tag wordpress-runner:latest registry.example.com/wordpress-runner:latest")
            click.echo("docker tag wordpress-actions-runner:latest registry.example.com/wordpress-actions-runner:latest")
            click.echo("docker push registry.example.com/wordpress:latest")
            click.echo("docker push registry.example.com/wordpress-runner:latest")
            click.echo("docker push registry.example.com/wordpress-actions-runner:latest")
            click.echo("\nUse the following helm commands to install WordPress Enterprise:")
            click.echo("helm install wordpress ./wordpress.tgz ")
            click.echo("  --namespace wordpress ")
            click.echo("  --create-namespace ")
            click.echo("  --values wordpress.yaml\n")
            return
        registry_spinner = Halo(text='Waiting for registry info', spinner='dots')
        registry_spinner.start()
        time.sleep(config.get('sleep_interval', 3))
        if airgap_bundle or config.get('push_images', True):
            registry_spinner.text = 'Pushing images to registry'
            time.sleep(config.get('sleep_interval', 3))
        registry_spinner.succeed('Setup complete')
        install_spinner = Halo(text='Validating environment', spinner='dots')
        install_spinner.start()
        time.sleep(config.get('sleep_interval', 3))
        install_spinner.text = 'Installing WordPress Enterprise'
        time.sleep(config.get('sleep_interval', 3))
        install_spinner.succeed('Installation complete')

    if target == 'linux':
        registry_spinner = Halo(text='Waiting for setup info', spinner='dots')
        registry_spinner.start()
        time.sleep(config.get('sleep_interval', 3))
        if airgap_bundle or config.get('push_images', True):
            registry_spinner.text = 'Pushing images to registry'
            time.sleep(config.get('sleep_interval', 3))
        registry_spinner.text = 'Validating host requirements'
        time.sleep(config.get('sleep_interval', 3))
        registry_spinner.text = 'Setting up host'
        time.sleep(config.get('sleep_interval', 3))
        if config.get('multi_node', False):
            registry_spinner.text = 'Waiting for other hosts'
            time.sleep(config.get('sleep_interval', 3))
        registry_spinner.succeed('Setup complete')
        deploy_spinner = Halo(text='Installing storage', spinner='dots')
        deploy_spinner.start()
        time.sleep(config.get('sleep_interval', 3))
        deploy_spinner.text = 'Installing registry'
        time.sleep(config.get('sleep_interval', 3))
        deploy_spinner.text = 'Preparing disaster recovery'
        time.sleep(config.get('sleep_interval', 3))
        deploy_spinner.text = 'Installing additional components'
        time.sleep(config.get('sleep_interval', 3))
        deploy_spinner.text = 'Validating environment'
        time.sleep(config.get('sleep_interval', 3))
        deploy_spinner.text = 'Installing WordPress Enterprise'
        time.sleep(config.get('sleep_interval', 3))
        deploy_spinner.succeed('Installation complete')

    click.echo('\nWordPress Enterprise installed successfully.\n')
    click.echo('The Admin Console is available at:')
    click.echo('https://shorturl.at/7gpFW\n')

# UPGRADE COMMAND
@cli.command()
@click.option('--airgap-bundle', type=click.Path(exists=True), help='Path to airgap bundle file')
@click.option('--cert-file', type=click.Path(exists=True), help='Path to certificate file for securing WordPress Enterprise manager access')
@click.option('--dry-run', is_flag=True, help='Show the upgrade commands instead of executing them')
@click.option('--key-file', type=click.Path(exists=True), help='Path to private key file for securing WordPress Enterprise manager access')
@click.option('--license', '-l', 'license_path', type=click.Path(exists=True), help='Path to a license file (required for airgap installations)')
@click.option('--target', type=click.Choice(['kubernetes', 'linux']), required=True, help='Deployment target')
@click.option('-y', '--yes', is_flag=True, help='Answer yes to all prompts')
def upgrade(dry_run, airgap_bundle, license_path, key_file, cert_file, target, yes):
    """Upgrade WordPress Enterprise"""
    config = load_config()
    
    # Validate license is provided for airgap installations
    if airgap_bundle and not license_path:
        click.echo(click.style("\nLicense file is required for airgap installations.", fg='red'))
        click.echo("Please provide a license file using the --license flag.\n")
        return
    
    if key_file and cert_file:
        click.echo("\nCertificate has been updated.")
    
    click.echo("\nVisit the WordPress Enterprise manager to continue:")
    click.echo("https://shorturl.at/c21df")
    time.sleep(config.get('sleep_interval', 3))
    click.echo("")
    wait_text = 'Waiting for configuration'
    wait_spinner = Halo(text=f'{wait_text}', spinner='dots')
    wait_spinner.start()
    time.sleep(config.get('sleep_interval', 3))
    wait_spinner.succeed('Configuration complete')

    if target == 'kubernetes':
        if dry_run:
            file_spinner = Halo(text='Preparing files', spinner='dots')
            file_spinner.start()
            with open('wordpress.tgz', 'wb') as f:
                f.write(b'')
            with open('wordpress.yaml', 'w') as f:
                f.write('# values.yaml for wordpress\n')
            time.sleep(config.get('sleep_interval', 3))
            file_spinner.succeed('Files prepared')
            click.echo("\nUse the following docker commands to load and push the images:")
            if airgap_bundle:
                click.echo(f"docker load -i {airgap_bundle}")
            else:
                click.echo("docker pull images.wordpress.com/proxy/wordpress/wordpress:latest")
                click.echo("docker pull images.wordpress.com/proxy/wordpress/wordpress-runner:latest")
                click.echo("docker pull images.wordpress.com/proxy/wordpress/wordpress-actions-runner:latest")
            click.echo("docker tag wordpress:latest registry.example.com/wordpress:latest")
            click.echo("docker tag wordpress-runner:latest registry.example.com/wordpress-runner:latest")
            click.echo("docker tag wordpress-actions-runner:latest registry.example.com/wordpress-actions-runner:latest")
            click.echo("docker push registry.example.com/wordpress:latest")
            click.echo("docker push registry.example.com/wordpress-runner:latest")
            click.echo("docker push registry.example.com/wordpress-actions-runner:latest")
            click.echo("\nUse the following helm commands to upgrade WordPress Enterprise:")
            click.echo("helm upgrade wordpress ./wordpress.tgz ")
            click.echo("  --namespace wordpress ")
            click.echo("  --values wordpress.yaml\n")
            return
        registry_spinner = Halo(text='Waiting for registry info', spinner='dots')
        registry_spinner.start()
        time.sleep(config.get('sleep_interval', 3))
        if airgap_bundle or config.get('push_images', True):
            registry_spinner.text = 'Pushing images to registry'
            time.sleep(config.get('sleep_interval', 3))
        registry_spinner.succeed('Setup complete')
        upgrade_spinner = Halo(text='Validating environment', spinner='dots')
        upgrade_spinner.start()
        time.sleep(config.get('sleep_interval', 3))
        upgrade_spinner.text = 'Upgrading WordPress Enterprise'
        time.sleep(config.get('sleep_interval', 3))
        upgrade_spinner.succeed('Upgrade complete')

    if target == 'linux':
        registry_spinner = Halo(text='Waiting for registry info', spinner='dots')
        registry_spinner.start()
        time.sleep(config.get('sleep_interval', 3))
        if airgap_bundle or config.get('push_images', True):
            registry_spinner.text = 'Pushing images to registry'
            time.sleep(config.get('sleep_interval', 3))
        registry_spinner.succeed('Setup complete')
        upgrade_spinner = Halo(text='Validating environment', spinner='dots')
        upgrade_spinner.start()
        time.sleep(config.get('sleep_interval', 3))
        upgrade_spinner.text = 'Upgrading WordPress Enterprise'
        time.sleep(config.get('sleep_interval', 3))
        upgrade_spinner.succeed('Upgrade complete')

    click.echo('\nWordPress Enterprise upgraded successfully.\n')
    click.echo('The Admin Console is available at:')
    click.echo('https://shorturl.at/7gpFW\n')

# ENABLE_HA GROUP
@cli.command()
def enable_ha():
    """Enable high availability on linux cluster"""
    config = load_config()
    click.echo("")
    spinner = Halo(text='Enabling high availability', spinner='dots')
    spinner.start()
    time.sleep(config.get('sleep_interval', 3))
    spinner.text = 'Migrating data'
    time.sleep(config.get('sleep_interval', 3))
    spinner.succeed('High availability enabled')
    click.echo("\nHigh availability enabled successfully.")
    click.echo("You must maintain at least three controller nodes to ensure high availability.\n")

# SHELL GROUP
@cli.command()
def shell():
    """Start a shell with WordPress binaries in PATH (Linux only)"""
    config = load_config()
    click.echo("\nStarting shell with WordPress binaries in PATH...")
    click.echo("Type 'exit' to return to the previous shell.\n")
    shell = os.environ.get('SHELL', '/bin/bash')
    import pty
    pty.spawn([shell, '-i', '-c', 'export PATH=\"/var/lib/wordpress/bin:$PATH\" && exec $SHELL'])

@cli.command()
def uninstall():
    """Remove WordPress Enterprise"""
    config = load_config()
    
    # Confirm the uninstall
    if not click.confirm("\nThis will uninstall WordPress Enterprise from this node. Are you sure?", default=False):
        click.echo("\nUninstall cancelled.\n")
        return
    click.echo("")
    # Show uninstall spinner
    spinner = Halo(text='Uninstalling WordPress Enterprise', spinner='dots')
    spinner.start()
    time.sleep(config.get('sleep_interval', 3))
    spinner.succeed('Uninstall complete')
    
    click.echo("\nYou can now run the install command to start fresh.\n")

@cli.command()
def support_bundle():
    """Generate a support bundle for troubleshooting"""
    config = load_config()
    click.echo("")  # Add initial newline
    spinner = Halo(text='Generating support bundle', spinner='dots')
    spinner.start()
    
    # Simulate bundle generation
    time.sleep(config.get('sleep_interval', 3))
    
    # Create a timestamped bundle directory
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    bundle_dir = f"wordpress-support-bundle-{timestamp}"
    os.makedirs(bundle_dir, exist_ok=True)
    
    # Simulate creating bundle files
    with open(os.path.join(bundle_dir, 'logs.txt'), 'w') as f:
        f.write("Sample log content\n")
    with open(os.path.join(bundle_dir, 'config.yaml'), 'w') as f:
        f.write("Sample configuration\n")
    with open(os.path.join(bundle_dir, 'system-info.txt'), 'w') as f:
        f.write("Sample system information\n")
    
    # Create a tar.gz file of the bundle
    import tarfile
    bundle_tgz = f"{bundle_dir}.tgz"
    with tarfile.open(bundle_tgz, 'w:gz') as tar:
        for root, _, files in os.walk(bundle_dir):
            for file in files:
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=os.path.relpath(file_path, bundle_dir))
    
    # Clean up the directory
    import shutil
    shutil.rmtree(bundle_dir)
    
    spinner.succeed('Support bundle generated')
    
    # Show where the bundle was saved
    bundle_path = os.path.abspath(bundle_tgz)
    click.echo(f"\nSupport bundle saved to {bundle_path}")
    
    # Ask if they want to send the bundle to support
    if click.confirm("\nWould you like to send this bundle to support?", default=True):
        click.echo("")
        spinner = Halo(text='Uploading support bundle', spinner='dots')
        spinner.start()
        time.sleep(config.get('sleep_interval', 3))
        spinner.succeed('Support bundle sent to support')
        click.echo("\nVisit the enterprise portal to view your support bundle.\n")
    else:
        click.echo("\nYou can send the bundle to support later by running this command again.\n")

@cli.command()
@click.option('--license', '-l', 'license_path', type=click.Path(exists=True), required=True, help='Path to a license file')
def configure(license_path):
    """Configure WordPress Enterprise"""
    config = load_config()
    
    click.echo("\nVisit the configuration wizard to continue:")
    click.echo("https://shorturl.at/c21df")
    
    # Wait before showing the configuration spinner
    time.sleep(config.get('sleep_interval', 3))
    
    click.echo("")
    
    # Start a new spinner for the waiting state
    wait_text = 'Waiting for configuration'
    wait_spinner = Halo(text=f'{wait_text}', spinner='dots')
    wait_spinner.start()
    time.sleep(config.get('sleep_interval', 3))
    wait_spinner.succeed('Configuration complete')
    
    # Write ConfigValues file
    config_values = {
        'apiVersion': 'kots.io/v1beta1',
        'kind': 'ConfigValues',
        'spec': {
            'values': {
                'hostname': {
                    'value': 'wordpress.example.com'
                },
                'admin_password': {
                    'valuePlaintext': 'admin123'
                },
                'smtp_enabled': {
                    'value': '1'
                },
                'smtp_host': {
                    'value': 'smtp.example.com'
                }
            }
        }
    }
    
    with open('config-values.yaml', 'w') as f:
        yaml.dump(config_values, f, default_flow_style=False)
    
    config_path = os.path.abspath('config-values.yaml')
    click.echo(f"\nConfig values saved to {config_path}\n")

@cli.command()
@click.option('-y', '--yes', is_flag=True, help='Answer yes to all prompts')
@click.option('--version', help='Specific version to update to')
def update(yes, version):
    """Update the WordPress CLI to the latest version"""
    if version:
        # Validate version format
        try:
            target_version = packaging_version.parse(version)
        except Exception:
            click.echo(click.style("\nInvalid version format. Please use semantic versioning (e.g. 1.2.3)", fg='red'))
            return
        
        if target_version <= packaging_version.parse(CURRENT_VERSION):
            click.echo(click.style(f"\nVersion {version} is not newer than current version {CURRENT_VERSION}", fg='yellow'))
            if not yes and not click.confirm("\nDo you want to downgrade?", default=False):
                click.echo("\nUpdate cancelled.\n")
                return
    else:
        latest_version = check_for_updates()
        if not latest_version:
            click.echo("\nYou are already running the latest version.")
            return
        version = latest_version

    click.echo(f"\nUpdating to version {version}")
    click.echo("")
    # Start update spinner
    spinner = Halo(text='Downloading new version', spinner='dots')
    spinner.start()
    
    # Simulate update process
    time.sleep(2)
    spinner.text = 'Installing update'
    time.sleep(2)
    
    spinner.succeed('Update complete')
    click.echo(f"\nCLI has been updated to version {version}")
    click.echo("You can now run 'wordpress upgrade' to upgrade WordPress Enterprise.\n")

@cli.command()
@click.option('--manager-password', required=True, help='Password for accessing the WordPress Enterprise manager')
def join(manager_password):
    """Join a new node to the linux cluster"""
    config = load_config()
    click.echo("")
    spinner = Halo(text='Joining node to cluster', spinner='dots')
    spinner.start()
    time.sleep(config.get('sleep_interval', 3))
    spinner.text = 'Waiting for node'
    time.sleep(config.get('sleep_interval', 3))
    spinner.succeed('Node joined the cluster')
    click.echo("\nNode joined the cluster successfully.\n")

if __name__ == '__main__':
    cli()