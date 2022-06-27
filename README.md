# PyQJsonModel
JSON Tree Model inspired by https://github.com/dridk/QJsonModel

Little helper classes for displaying JSON Data in a QTreeModel. Just run the File for a Demo. Use this model together with JSON-data as binary, from a file or a dict as data-source.

`QJsonModel - update_data(json_dict_or_filename)
` now supports json-data, a dict or a filename.

You need Python3(>=3.8) and PySide2 (>=5.14) installed. This is what I used at the moment of coding. Could also work in other configurations.

Update 2021-01-24: Model supports editing. The current, edited value can be retrieved by the property `as_dict` from the model. Tested with Python 3.9.1 and PySide2 5.15.2

Update 2022-06-27: Minor cleanup. Tested with Python 3.9.13

Any comments welcome to info{at}rabotix.de
