import re


class CsvFileNameValidator:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file

    def validate(self):
        if not self.csv_file.endswith(".csv"):
            raise ValueError("拡張子が.csvではありません")

        table_name = self.csv_file.removesuffix(".csv")

        if not table_name:
            raise ValueError("ファイル名が空です")

        invalid_chars = re.findall(r'[^a-zA-Z0-9_\-]', table_name)
        if invalid_chars:
            formatted = ''.join(f'「スペース」' if c == ' ' else f'「{c}」' for c in set(invalid_chars))
            raise ValueError(f"{formatted}は使用できません")
