import yaml


class DotDict(dict):
    """
    'dot.notation' 액세스를 할 수 있는 dict를 만들어주는 클래스
    중첩된 딕셔너리도 dot notation으로 접근 가능
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DotDict(value)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return DotDict(config)
