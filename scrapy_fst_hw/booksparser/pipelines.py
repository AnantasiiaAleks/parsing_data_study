# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import re
from w3lib.html import remove_tags
from urllib.parse import unquote


class BooksparserPipeline:
    def __init__(self):
        self.file = None
        self.writer = None

    def open_spider(self, spider):
        """Создать файл с именем паука. """
        filename = f"{spider.name}_books.csv"  # имя файла = имя паука
        try:
            self.file = open(filename, 'w', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            # Заголовки
            self.writer.writerow(['_id', 'title', 'price', 'description', 'url'])
            spider.logger.info(f"CSV файл создан: {filename}")
        except Exception as e:
            spider.logger.error(f"Не удалось создать файл {filename}: {e}")
            raise e


    def close_file(self, spider):
        """Закрыть файл при завершении работы паука"""
        if self.file:
            self.file.close()


    def process_item(self, item, spider):
        # Извлечение и очистка данных
        _id = self._get_joined(item.get('_id', '')).strip()
        title = self._get_joined(item.get('title', '')).strip()
        raw_price = self._get_joined(item.get('price', ''))
        description = self._get_joined(item.get('description', '')).strip()
        url = self._get_joined(item.get('url', '')).strip()

        price = self._clean_price(raw_price)

        # Записать строку в CSV
        self.writer.writerow([_id, title, price, description, url])
        self.file.flush()

        return item


    def _get_joined(self, value, separator=' '):
        """
        Превращает список или строку в чистую строку.
        Удаляет лишние пробелы, переносы, дубли.
        """
        if value is None:
            return ''
        if isinstance(value, list):
            parts = [re.sub(r'\s+', ' ', x.strip()) for x in value if x.strip()]
            return separator.join(parts)
        return re.sub(r'\s+', ' ', str(value).strip())


    def _clean_price(self, price_str):
        """
        Очищает строку цены и конвертирует в float.
        Пример: '1&nbsp;072' → 1072.0
        """
        if not price_str:
            return None

        # Декодирование HTML-сущностей, например &nbsp; → пробел
        price_str = remove_tags(price_str)  # если есть теги
        price_str = unquote(price_str)     # URL-кодировка
        price_str = price_str.replace('\xa0', ' ')  # &nbsp; → пробел
        price_str = re.sub(r'[^\d,\.]', '', price_str)  # оставить только цифры, точки, запятые

        # Заменить запятую на точку, если это разделитель дробной части
        price_str = price_str.replace(',', '.')

        # Убрать лишние точки (оставляем только первую как десятичную)
        parts = price_str.split('.')
        if len(parts) > 2:
            price_str = ''.join(parts[:-1]) + '.' + parts[-1]  # только одна точка — в конце

        try:
            return float(price_str) if price_str else None
        except ValueError:
            return None