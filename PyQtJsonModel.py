# 2017-2020 by Gregor Engberding , MIT License
import logging
import sys

from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt, QJsonDocument, QJsonParseError
from PySide2.QtWidgets import QApplication, QTreeView

DEMO_JSON = b"""{
                   "firstName": "John",
                   "lastName": "Smith",
                   "age": 25,
                   "address":
                   {
                       "streetAddress": "21 2nd Street",
                       "city": "New York",
                       "state": "NY",
                       "postalCode": "10021"
                   },
                   "phoneNumber":
                   [
                       {
                         "type": "home",
                         "number": "212 555-1234"
                       },
                       {
                         "type": "fax",
                         "number": "646 555-4567"
                       }
                   ]
               }"""

DEMO_DICT = {
    "firstName"  : "John",
    "lastName"   : "Smith",
    "age"        : 25,
    "address"    :
        {
            "streetAddress": "21 2nd Street",
            "city"         : "New York",
            "state"        : "NY",
            "postalCode"   : "10021"
            },
    "phoneNumber":
        [
            {
                "type"  : "home",
                "number": "212 555-1234"
                },
            {
                "type"  : "fax",
                "number": "646 555-4567"
                }
            ]
    }


class QJsonTreeItem:
    """A tree node with parent and children

    For easy display by the QJsonModel

    """

    def __init__(self, parent=None, value=None):

        self.parent = parent
        self.children = []
        self.value = None
        self.key = None
        self.typename = None

        if value:
            self.init_tree(value, parent)

    def row(self):
        """Special for Qt, the row(aka. index) in it´s parent children

        :return: Own index in parent´s children or -1
        """
        if self.parent is not None:
            return self.parent.children.index(self)
        return -1

    def init_tree(self, value, parent=None):
        """Initializes the tree below parent with value

        :param value: the value to be inserted below parent
        :param parent: insert value below this parent, if None, it´s the root node
        :return: the tree-structure of QJsonTreeItems
        """
        root_item = QJsonTreeItem(parent=parent)
        root_item.key = "root"

        if isinstance(value, dict):
            for key, val in value.items():
                child = self.init_tree(val, root_item)
                child.key = key
                root_item.children.append(child)

        elif isinstance(value, list):
            for idx, val in enumerate(value):
                child = self.init_tree(val, root_item)
                child.key = idx
                root_item.children.append(child)

        else:
            root_item.value = value

        root_item.typename = type(value).__name__
        return root_item


class QJsonModel(QAbstractItemModel):
    """To be used as a model with a QTreeView to show contents of a JSON

    """
    def __init__(self, parent=None, json_data=None):
        super().__init__(parent)
        self.document = None
        self.root_item = QJsonTreeItem()
        self.headers = ["key", "value", "type"]
        if json_data:
            self.update_data(json_data)

    def update_data(self, json_data):
        """New data for the model

        :param json_data: binary JSON, a dict or a filename
        :return:
        """
        error = QJsonParseError()
        try:
            self.document = QJsonDocument.fromJson(json_data, error)
        except TypeError:
            if isinstance(json_data, dict):
                self.document = QJsonDocument.fromVariant(json_data)

        if self.document is not None:
            self.beginResetModel()
            if self.document.isArray():
                self.root_item.init_tree(list(self.document.array()))
            else:
                self.root_item = self.root_item.init_tree(self.document.object())
            self.endResetModel()
            return

        else:
            # try as file
            print(f"from file")
            if self.load_from_file(filename=json_data):
                return

        msg = f"Unable to load as JSON:{json_data}"
        logging.log(logging.DEBUG, msg)
        raise ValueError(msg)

    def load_from_file(self, filename):
        """Loads JSON from filename

        :param filename: name of json-file
        :return: (bool) True=success, False=failed
        """
        if filename is None or filename is False:
            return False

        with open(filename, "rb") as file:
            if file is None:
                return False

            json_data = file.read()
            self.update_data(json_data)

        return True

    def data(self, index: QModelIndex, role: int = ...):
        if not index.isValid():
            return None

        item = index.internalPointer()
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:
                return item.key
            elif col == 1:
                value = item.value
                return value
            elif col == 2:
                return item.typename

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.headers[section]

        return None

    def index(self, row: int, column: int, parent: QModelIndex = ...):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        try:
            child_item = parent_item.children[row]
            return self.createIndex(row, column, child_item)
        except IndexError:
            return QModelIndex()

    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent

        if parent_item == self.root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: QModelIndex = ...):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        return len(parent_item.children)

    def columnCount(self, parent: QModelIndex = ...):
        return 3


if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = QJsonModel(json_data=DEMO_JSON)

    # or use a dict as data-source
    # model = QJsonModel(json_data=DEMO_DICT)

    # or use a filename
    # model = QJsonModel(json_data="json-data.json")

    view = QTreeView()
    view.setModel(model)
    view.show()

    sys.exit(app.exec_())
