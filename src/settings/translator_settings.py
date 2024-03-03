"""
This file is part of SSE Auto Translator
by Cutleast and falls under the license
Attribution-NonCommercial-NoDerivatives 4.0 International.
"""

import qtawesome as qta
import qtpy.QtCore as qtc
import qtpy.QtWidgets as qtw

from translator_api import AVAILABLE_APIS

from widgets import KeyEntry

from main import MainApp


class TranslatorSettings(qtw.QWidget):
    """
    Widget for translator API settings.
    """

    on_change_signal = qtc.Signal()
    """
    This signal gets emitted every time
    the user changes some setting.
    """

    def __init__(self, app: MainApp):
        super().__init__()

        self.app = app
        self.loc = app.loc
        self.mloc = app.loc.settings

        self.setObjectName("root")

        flayout = qtw.QFormLayout()
        self.setLayout(flayout)

        # Translator
        self.translator_box = qtw.QComboBox()
        self.translator_box.setEditable(False)
        self.translator_box.addItems([translator.name for translator in AVAILABLE_APIS])
        self.translator_box.setCurrentText(self.app.translator_config["translator"])
        self.translator_box.currentTextChanged.connect(self.on_change)
        flayout.addRow(self.mloc.translator, self.translator_box)

        # API Key
        api_key_label = qtw.QLabel(self.mloc.translator_api_key)
        self.api_key_entry = KeyEntry()
        self.api_key_entry.setDisabled(True)
        self.api_key_entry.textChanged.connect(self.on_change)
        if self.app.translator_config["api_key"]:
            self.api_key_entry.setText(self.app.translator_config["api_key"])
            self.api_key_entry.setDisabled(False)
        flayout.addRow(api_key_label, self.api_key_entry)

        self.translator_box.currentTextChanged.connect(
            lambda text: (
                self.api_key_entry.setEnabled(text == "DeepL"),
                api_key_label.setEnabled(text == "DeepL"),
            )
        )

    def on_change(self, *args):
        """
        This emits change signal without passing parameters.
        """

        self.on_change_signal.emit()

    def get_settings(self):
        api_key = self.api_key_entry.text() if self.api_key_entry.text() else None

        return {
            "translator": self.translator_box.currentText(),
            "api_key": api_key,
        }
