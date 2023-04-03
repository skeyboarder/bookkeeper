"""
Тесты GUI для главного окна
"""

from pytestqt.qt_compat import qt_api

from bookkeeper.view.main_window import MainWindow
from bookkeeper.view.budget import BudgetTableGroup
from bookkeeper.view.new_expense import NewExpenseGroup
from bookkeeper.view.expenses import ExpensesTableGroup


def modifier(pk, val1, val2): return None
def pk_to_name(pk): return ""
def deleter(pks): return None
def cats_edit_show(): return None
def adder(amount, name, comment): return None


def test_create_window(qtbot):
    budget_table = BudgetTableGroup(modifier)
    new_expense = NewExpenseGroup([], cats_edit_show, adder)
    expenses_table = ExpensesTableGroup(pk_to_name, modifier, deleter)
    window = MainWindow(budget_table, new_expense, expenses_table)
    qtbot.addWidget(window)
    assert window.budget_table == budget_table
    assert window.new_expense == new_expense
    assert window.expenses_table == expenses_table


def test_change_theme(qtbot):
    budget_table = BudgetTableGroup(modifier)
    new_expense = NewExpenseGroup([], cats_edit_show, adder)
    expenses_table = ExpensesTableGroup(pk_to_name, modifier, deleter)
    window = MainWindow(budget_table, new_expense, expenses_table)
    qtbot.addWidget(window)
    assert window.is_dark_mode is True
    window.theme.check_box.setCheckState(qt_api.QtCore.Qt.Unchecked)
    assert window.is_dark_mode is False
    window.theme.check_box.setCheckState(qt_api.QtCore.Qt.Checked)
    assert window.is_dark_mode is True


def test_close_event(qtbot, monkeypatch):
    for result, msg in zip(
        [True, False],
        [qt_api.QtWidgets.QMessageBox.Yes, qt_api.QtWidgets.QMessageBox.No]
    ):
        budget_table = BudgetTableGroup(modifier)
        new_expense = NewExpenseGroup([], cats_edit_show, adder)
        expenses_table = ExpensesTableGroup(pk_to_name, modifier, deleter)
        window = MainWindow(budget_table, new_expense, expenses_table)
        qtbot.addWidget(window)
        monkeypatch.setattr(qt_api.QtWidgets.QMessageBox,
                            "question", lambda *args: msg)
        assert window.close() is result
