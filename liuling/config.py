from pathlib import Path

import yaml


class Configuration:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        yaml.add_constructor('!Configuration', self.__from_yaml__)

        # 记载YAML文件
        with self.config_path.open('r', encoding='utf-8') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

            self.checker = self.config["checker"]
            self.ratio = self.config['ratio']

    @staticmethod
    def __from_yaml__(loader, node):
        return loader.construct_mapping(node)


if __name__ == "__main__":
    config = Configuration("./config.yaml")
    print(config.config)
