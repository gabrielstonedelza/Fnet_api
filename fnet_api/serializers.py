from django.db.models import fields
from rest_framework import serializers
from .models import (Customer, CustomerWithdrawal, MyPayments, AdminAccountsStartedWith, CashAtPayments,
                     WithdrawReference, AdminAccountsCompletedWith, CustomerAccounts, CustomerRequestDeposit,
                     ExpensesRequest, MobileMoneyDeposit, BankDeposit, UserMobileMoneyAccountsStarted,
                     UserMobileMoneyAccountsClosed, MobileMoneyWithdraw, Notifications)


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Customer
        fields = ['id', 'agent', 'username', 'name', 'location', 'digital_address', 'phone',
                  'date_of_birth', 'date_created']
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class CustomerAccountsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = CustomerAccounts
        fields = ['id', 'agent', 'username', 'account_number', 'account_name', 'bank', 'phone', 'date_added']
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class CustomerDepositRequestSerializer(serializers.ModelSerializer):
    agent_username = serializers.SerializerMethodField('get_agent_username')

    class Meta:
        model = CustomerRequestDeposit
        fields = ['id', 'customer_phone', 'agent', 'customer_name', 'agent_username',
                  'amount', 'request_option', 'request_status', 'date_requested', 'time_requested', 'slug']

    def get_agent_username(self, user):
        agent_username = user.agent.username
        return agent_username


class ExpenseRequestSerializer(serializers.ModelSerializer):
    guarantor_username = serializers.SerializerMethodField('get_guarantor_username')
    agent_username = serializers.SerializerMethodField('get_agent_username')

    class Meta:
        model = ExpensesRequest
        fields = ['id', 'guarantor', 'agent', 'guarantor_username', 'deposit_paid',
                  'agent_username', 'amount', 'reason', 'request_status', 'date_requested', 'time_requested', 'slug']
        read_only_fields = ['agent']

    def get_guarantor_username(self, user):
        guarantor_username = user.guarantor.username
        return guarantor_username

    def get_agent_username(self, user):
        agent_username = user.agent.username
        return agent_username


class MobileMoneyDepositSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = MobileMoneyDeposit
        fields = ['id', 'agent', 'customer_phone', 'customer_name', 'username', 'network', 'type', 'amount', 'charges',
                  'agent_commission', 'date_deposited', 'time_deposited']
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class BankDepositSerializer(serializers.ModelSerializer):
    guarantor_username = serializers.SerializerMethodField('get_guarantor_username')
    customer_username = serializers.SerializerMethodField('get_customer_username')
    agent_username = serializers.SerializerMethodField('get_agent_username')

    class Meta:
        model = BankDeposit
        fields = ['id', 'guarantor', 'customer', 'agent', 'guarantor_username', 'customer_username', 'deposit_paid',
                  'agent_username', 'bank', 'account_number', 'account_name', 'amount', 'request_status',
                  'date_requested', 'time_requested', 'slug']
        read_only_fields = ['agent']

    def get_guarantor_username(self, user):
        guarantor_username = user.guarantor.username
        return guarantor_username

    def get_customer_username(self, user):
        customer_username = user.customer
        return customer_username

    def get_agent_username(self, user):
        agent_username = user.agent.username
        return agent_username


class CustomerWithdrawalSerializer(serializers.ModelSerializer):
    customer_username = serializers.SerializerMethodField('get_customer_username')
    agent_username = serializers.SerializerMethodField('get_agent_username')

    class Meta:
        model = CustomerWithdrawal
        fields = ['id', 'agent', 'customer', 'customer_username', 'agent_username', 'bank', 'amount', 'date_requested']
        read_only_fields = ['agent']

    def get_customer_username(self, user):
        customer_username = user.customer
        return customer_username

    def get_agent_username(self, user):
        agent_username = user.agent.username
        return agent_username


class PaymentsSerializer(serializers.ModelSerializer):
    agent_username = serializers.SerializerMethodField('get_agent_username')

    class Meta:
        model = MyPayments
        fields = ['id', 'agent', 'agent_username', 'mode_of_payment1', 'mode_of_payment2', 'cash_at_location1',
                  'cash_at_location2', 'amount', 'amount1', 'amount2', 'bank1', 'bank2', 'transaction_id1',
                  'transaction_id2', 'payment_action', 'payment_status', 'date_created', 'time_created', 'slug']
        read_only_fields = ['agent']

    def get_agent_username(self, user):
        agent_username = user.agent.username
        return agent_username


class AdminAccountsStartedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = AdminAccountsStartedWith
        fields = ['id', 'user', 'username', 'physical_cash', 'eCash', 'date_started']
        read_only_fields = ['user']

    def get_username(self, mm_user):
        username = mm_user.user.username
        return username


class AdminAccountsCompletedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = AdminAccountsCompletedWith
        fields = ['id', 'user', 'username', 'physical_cash', 'eCash', 'date_closed']
        read_only_fields = ['user']

    def get_username(self, mm_user):
        username = mm_user.user.username
        return username


class CashAtPaymentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = CashAtPayments
        fields = ['id', 'agent', 'username', 'location', 'amount', 'left_with', 'left_with_phone', 'reference_id',
                  'date_paid', 'time_paid']
        read_only_fields = ['agent']

    def get_username(self, mm_user):
        username = mm_user.agent.username
        return username


class WithdrawSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = WithdrawReference
        fields = ['id', 'agent', 'username', 'amount', 'reference_id', 'customer_phone', 'date_withdrew',
                  'time_withdrew']
        read_only_fields = ['agent']

    def get_username(self, mm_user):
        username = mm_user.agent.username
        return username


class UserMobileMoneyAccountsStartedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = UserMobileMoneyAccountsStarted
        fields = ['id', 'agent', 'username', 'physical', 'mtn_ecash', 'tigoairtel_ecash', 'vodafone_ecash',
                  'ecash_total', 'date_posted']
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class UserMobileMoneyAccountsClosedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = UserMobileMoneyAccountsClosed
        fields = ['id', 'agent', 'username', 'physical', 'mtn_ecash', 'tigoairtel_ecash', 'vodafone_ecash',
                  'ecash_total', 'date_posted']
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class MobileMoneyWithdrawalSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = MobileMoneyWithdraw
        fields = ['id', 'agent', 'username', 'customer_phone', 'customer_name', 'network', 'type', 'id_type',
                  'id_number', 'amount', 'charges', 'agent_commission', 'cash_out_commission', 'mtn_commission',
                  'date_of_withdrawal', 'time_of_withdrawal']
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'item_id', 'transaction_type', 'notification_title', 'notification_message',
                  'notification_trigger', 'read', 'customer', 'user', 'user2', 'customer_request_slug',
                  'cash_deposit_request_slug', 'bank_deposit_request_slug', 'payment_slug', 'date_created', 'slug']
