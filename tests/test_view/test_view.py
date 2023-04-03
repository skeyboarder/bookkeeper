"""
Тесты View из модели MVP
"""

from pytestqt.qt_compat import qt_api

from bookkeeper.view.view import View, handle_error
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


def test_set_categories():
    view = View()
    for cats in [[],
                 [Category("cat1", pk=1),
                  Category("cat2", pk=2)]]:
        view.set_categories(cats)
        assert view.categories == cats


def test_catpk_to_name():
    view = View()
    cats = [Category("cat1", pk=1),
            Category("cat2", pk=2),]
    view.set_categories(cats)
    assert view.catpk_to_name(1) == "cat1"
    assert view.catpk_to_name(3) == ""


def test_set_expenses():
    view = View()
    exps = [Expense(100, 1, comment="test"),
            Expense(200, 2, expense_date="12.12.2012 15:30")]
    view.set_expenses(exps)
    assert view.expenses == exps
    assert view.expenses_table.expenses == exps


def test_set_budgets():
    view = View()
    bdgs = [Budget(1000, "day", spent=100),
            Budget(7000, "week"),]
    view.set_budgets(bdgs)
    assert view.budgets == bdgs
    assert view.budget_table.budgets == bdgs


def test_handle_error(qtbot, monkeypatch):
    def handler_err():
        raise ValueError('test')

    def handler_noerr():
        pass

    def monkey_func(*args):
        monkey_func.was_called = True
        return qt_api.QtWidgets.QMessageBox.Ok
    monkey_func.was_called = False
    widget = qt_api.QtWidgets.QWidget()
    qtbot.addWidget(widget)
    monkeypatch.setattr(qt_api.QtWidgets.QMessageBox,
                        "critical", monkey_func)
    handle_error(widget, handler_noerr)()
    assert monkey_func.was_called is False
    handle_error(widget, handler_err)()
    assert monkey_func.was_called is True


def test_set_handler(monkeypatch):
    view = View()

    def handler(*args):
        handler.call_count += 1
    handler.call_count = 0
    view.set_cat_adder(handler)
    view.add_category('name', 'parent')
    assert handler.call_count == 1
    view.set_cat_modifier(handler)
    view.modify_category('cat_name', 'new_name', 'new_parent')
    assert handler.call_count == 2
    view.set_cat_deleter(handler)
    view.delete_category('cat_name')
    assert handler.call_count == 3
    view.set_cat_checker(handler)
    view.cat_checker('cat_name')
    assert handler.call_count == 4
    view.set_bdg_modifier(handler)
    view.modify_budget(1, 'new_limit', 'period')
    assert handler.call_count == 5
    view.set_exp_adder(handler)
    view.add_expense('amount', 'cat_name')
    assert handler.call_count == 6
    monkeypatch.setattr(qt_api.QtWidgets.QMessageBox,
                        "question", lambda *args: qt_api.QtWidgets.QMessageBox.Yes)
    view.set_exp_deleter(handler)
    view.delete_expenses([1])
    assert handler.call_count == 7
    view.set_exp_modifier(handler)
    view.modify_expense(1, 'attr', 'new_val')
    assert handler.call_count == 8


def test_delete_expenses(monkeypatch):
    def deleter(*args):
        deleter.was_called = True
    deleter.was_called = False
    view = View()
    view.set_exp_deleter(deleter)

    def monkey_func_ok(*args):
        monkey_func_ok.was_called = True
        return qt_api.QtWidgets.QMessageBox.Ok
    monkey_func_ok.call_count = False
    monkeypatch.setattr(qt_api.QtWidgets.QMessageBox,
                        "critical", monkey_func_ok)
    view.delete_expenses([])
    assert monkey_func_ok.was_called is True
    assert deleter.was_called is False

    def monkey_func_no(*args):
        monkey_func_no.was_called = True
        return qt_api.QtWidgets.QMessageBox.No
    monkey_func_no.was_called = False
    monkeypatch.setattr(qt_api.QtWidgets.QMessageBox,
                        "question", monkey_func_no)
    view.delete_expenses([1])
    assert monkey_func_no.was_called is True
    assert deleter.was_called is False

    def monkey_func_yes(*args):
        monkey_func_yes.was_called = True
        return qt_api.QtWidgets.QMessageBox.Yes
    monkey_func_yes.was_called = False
    monkeypatch.setattr(qt_api.QtWidgets.QMessageBox,
                        "question", monkey_func_yes)
    view.delete_expenses([1])
    assert monkey_func_yes.was_called is True
    assert deleter.was_called is True


def test_death(monkeypatch):
    def monkey_func(*args):
        monkey_func.was_called = True
        return qt_api.QtWidgets.QMessageBox.Ok
    monkey_func.was_called = False
    view = View()
    monkeypatch.setattr(qt_api.QtWidgets.QMessageBox,
                        "warning", monkey_func)
    view.death()
    assert monkey_func.was_called is True
