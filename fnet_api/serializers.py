from django.db.models import fields
from rest_framework import serializers
from .models import (Customer, CustomerWithdrawal, MyPayments, AdminAccountsStartedWith, CashAtPayments, ExpensesRequest, CashRequest, MyCashPayments,
                     AdminAccountsCompletedWith, CustomerAccounts, CustomerRequestDeposit, WithdrawalReference,
                     MobileMoneyDeposit, BankDeposit, UserMobileMoneyAccountsStarted,
                     UserMobileMoneyAccountsClosed, MobileMoneyWithdraw, Notifications, PaymentAtBank, OTP, AccountNumberWithPoints,
                     CustomerPaymentAtBank, AddedToApprovedDeposits, AddedToApprovedPayment, Reports,
                     FnetPrivateUserMessage, FnetGroupMessage, PrivateChatId, AddToCustomerRequestToRedeemPoints, AddedToApprovedCashPayment, AuthenticateAgentPhone, AgentAndOwnerAccounts, Commercials, CustomerPoints,
                     AddToCustomerRedeemPoints, ReferCustomer, AddToBlockList)


class CustomerPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPoints
        fields = ['id','phone','name','points','points_active','date_added']


class CommercialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commercials
        fields = ['id','default_youtube_link','ecobank_youtube_video_link','fidelity_youtube_video_link','calbank_youtube_video_link','mtn_youtube_video_link','date_added']
class AgentAndOwnerAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentAndOwnerAccounts
        fields = ['id','agent','account_number','account_name','mtn_linked_number','bank','date_added','phone']
        read_only_fields = ['agent']
class AccountNumberWithPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountNumberWithPoints
        fields = ['id','agent','account_number','customer','account_name','date_deposited','time_deposited','points','bank','deposited_month','deposited_year','get_agent_username']
        read_only_fields =['agent']

class AuthenticateAgentPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticateAgentPhone
        fields = ['id','agent','phone_id','phone_model','phone_brand','finger_print','phone_authenticated','date_authenticated','get_agent_unique_code','get_agent_username']
        read_only_fields = ['agent']

class WithdrawalReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalReference
        fields = ['id','agent','amount','reference','date_added','get_username']
        read_only_fields = ['agent']
class AddToBlockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToBlockList
        fields = ['id', 'administrator', 'user', 'date_blocked', 'get_username']


class AddedToApprovedPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddedToApprovedPayment
        fields = ['id', 'payment', 'date_approved']


class AddedToApprovedBankDepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddedToApprovedDeposits
        fields = ['id', 'bank_deposit', 'date_approved']


class PaymentAtBankSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = PaymentAtBank
        fields = ['id', 'agent', 'username', 'teller_name', 'teller_phone', 'amount', 'total', 'd_200', 'd_100', 'd_50',
                  'd_20', 'd_10', 'd_5', 'd_2', 'd_1', 'date_added', 'time_added', ]
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Customer
        fields = ['id', 'agent', 'administrator', 'username', 'name', 'location', 'digital_address', 'id_type',
                  'id_number', 'phone', 'points', 'status',
                  'date_of_birth', 'date_created', 'get_agents_phone', 'referral']
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class AdminCustomerSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Customer
        fields = ['id', 'agent', 'administrator', 'username', 'name', 'location', 'digital_address', 'id_type',
                  'id_number', 'phone', 'points', 'status',
                  'date_of_birth', 'date_created', 'get_agents_phone', 'referral']

    def get_username(self, user):
        username = user.agent.username
        return username


class ReferCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferCustomer
        fields = ['id', 'administrator', 'name', 'phone', 'date_created', 'referral']


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
                  'amount', 'bank', 'request_status', 'date_requested',
                  'time_requested', 'slug']

    def get_agent_username(self, user):
        agent_username = user.agent.username
        return agent_username


class ExpenseRequestSerializer(serializers.ModelSerializer):
    guarantor_username = serializers.SerializerMethodField('get_guarantor_username')
    agent_username = serializers.SerializerMethodField('get_agent_username')

    class Meta:
        model = ExpensesRequest
        fields = ['id', 'guarantor', 'agent', 'guarantor_username', 'deposit_paid',
                  'agent_username', 'amount', 'reason', 'request_status', 'date_requested', 'time_requested',
                  ]
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
        fields = ['id', 'agent', 'customer_phone', 'username', 'network', 'type', 'amount',
                  'depositor_name', 'depositor_number','reference',
                   'date_deposited', 'time_deposited', ]
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
        fields = ['id', 'guarantor', 'customer', 'agent', 'guarantor_username', 'customer_username', 'deposit_paid','user_location','user_local_district',
                  'agent_username', 'bank', 'account_number', 'account_name', 'amount', 'depositor_name',
                  'request_status','deposited_month','deposited_year',
                  'date_requested', 'time_requested', 'slug' ]
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
        fields = ['id', 'agent', 'customer', 'customer_username', 'agent_username', 'bank', 'amount', 'id_number',
                  'id_type', 'withdrawal_type',
                  'date_requested']
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
                  'transaction_id2', 'payment_action', 'payment_status', 'date_created', 'time_created', 'slug',
                  'payment_month', 'payment_year', ]
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
        fields = ['id', 'agent', 'username', 'customer_phone', 'network', 'type',  'amount',
                  'date_of_withdrawal', 'time_of_withdrawal', 'reference']
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'item_id', 'transaction_type', 'notification_title', 'notification_message',
                  'notification_trigger', 'read', 'customer', 'user', 'user2', 'customer_request_slug',
                  'cash_deposit_request_slug', 'bank_deposit_request_slug', 'payment_slug', 'date_created', 'slug',
                  'notification_from', 'notification_to_guarantor', 'notification_to_customer']


class OTPSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = OTP
        fields = ['id', 'guarantor', 'username', 'customer', 'agent', 'otp', ]
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class CustomerPaymentAtBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPaymentAtBank
        fields = ['id', 'customer', 'agent_name', 'amount', 'total', 'd_200', 'd_100', 'd_50',
                  'd_20', 'd_10', 'd_5', 'd_2', 'd_1', 'date_added', 'time_added', ]


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ['id', 'administrator', 'user', 'report', 'date_reported', 'time_reported', 'read','get_username']
        read_only_fields = ['user']


# public and private messages
class FnetGroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FnetGroupMessage
        fields = ['id', 'user', 'message', 'get_date', 'get_username', 'get_phone_number', 'timestamp']
        read_only_fields = ['user']


class FnetPrivateUserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FnetPrivateUserMessage
        fields = ['id', 'sender', 'receiver', 'private_chat_id', 'message', 'read', 'get_date',
                  'get_senders_username', 'get_receivers_username', 'timestamp', 'isSender', 'isReceiver']
        # read_only_fields = ['sender', 'receiver']


class PrivateChatIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChatId
        fields = ['id', 'chat_id', 'date_created']


class AddToCustomerRequestToRedeemPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToCustomerRequestToRedeemPoints
        fields = ['id', 'customer_phone','customer_name', 'points','redeemed', 'date_created']


class AddToCustomerRedeemPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToCustomerRedeemPoints
        fields = ['id', 'customer', 'customer_phone', 'points', 'date_created', 'redeem_option']


class CashRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRequest
        fields = ['id','administrator','agent1','agent2','amount','request_status','date_requested','requested_month','requested_year','time_requested','get_agent1_username','get_agent2_username','request_paid']

class CashPaymentsSerializer(serializers.ModelSerializer):
    agent_username = serializers.SerializerMethodField('get_agent_username')

    class Meta:
        model = MyCashPayments
        fields = ['id', 'agent', 'agent_username', 'mode_of_payment1', 'mode_of_payment2', 'cash_at_location1',
                  'cash_at_location2', 'amount', 'amount1', 'amount2', 'bank1', 'bank2', 'transaction_id1',
                  'transaction_id2', 'payment_action', 'payment_status', 'date_created', 'time_created', 'slug',
                  'payment_month', 'payment_year', ]
        read_only_fields = ['agent']

    def get_agent_username(self, user):
        agent_username = user.agent.username
        return agent_username

class AddedToApprovedCashPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddedToApprovedCashPayment
        fields = ['id', 'payment', 'date_approved']