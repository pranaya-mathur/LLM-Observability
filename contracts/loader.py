import yaml
from pathlib import Path


class ContractLoader:
    def __init__(self, contracts_path: str):
        self.contracts_path = Path(contracts_path)
        self.contracts = {}

    def load(self):
        registry_file = self.contracts_path / 'registry.yaml'

        with open(registry_file, 'r') as f:
            registry = yaml.safe_load(f)

        for entry in registry['contracts']:
            contract_path = self.contracts_path / entry['path']
            with open(contract_path, 'r') as cf:
                contract = yaml.safe_load(cf)
                self.contracts[contract['id']] = contract

        return self.contracts
