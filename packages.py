# packages.py
import pkg_resources

def install_packages():
    packages = [
        'tensorflow>=2.0.0',
        # other dependencies
    ]
    for package in packages:
        try:
            pkg_resources.require(package)
        except pkg_resources.DistributionNotFound:
            import subprocess
            subprocess.check_call(['pip', 'install', package])

if __name__ == '__main__':
    install_packages()