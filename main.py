from model.repository import BankRepository
from view.main_window import BankView
from controller.auth_controller import AuthController
from controller.customers_controller import CustomersController
from controller.register_controller import RegisterController
from controller.transfer_controller import TransferController
from controller.deposit_withdraw_controller import DepositWithdrawController


def main():
    # ۱. مقداردهی اولیه به لایه مدل (اتصال اتمیک به پایگاه داده)
    repo = BankRepository()

    # ۲. مقداردهی اولیه به لایه نما (پنجره گرافیکی ریشه)
    view = BankView()

    # ۳. نمونه‌سازی تفکیک‌شده از ساب‌کنترلرها (کاهش هم‌تنیدگی کدهای لایه کنترلر)
    auth_ctrl = AuthController(repo, view)
    customers_ctrl = CustomersController(repo, view)
    register_ctrl = RegisterController(repo, view)
    transfer_ctrl = TransferController(repo, view)
    deposit_withdraw_ctrl = DepositWithdrawController(repo, view)

    # ۴. سیم‌کشی و تزریق کنترلرها به تب‌های متناظر در لایه گرافیکی (Dependency Injection)
    view.wire_controllers(
        auth_ctrl=auth_ctrl,
        customers_ctrl=customers_ctrl,
        register_ctrl=register_ctrl,
        transfer_ctrl=transfer_ctrl,
        deposit_withdraw_ctrl=deposit_withdraw_ctrl
    )

    # ۵. استارت نهایی لایف‌سایکل و چرخه حیات نرم‌افزار بانکی صندوق
    view.start_app()


if __name__ == "__main__":
    main()