from rest_framework import serializers
from .models import Customer, AgentDepositRequests, CustomerWithdrawal, Payments, TwilioApi, AdminAccountsStartedWith, \
    AdminAccountsCompletedWith


class TwilioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwilioApi
        fields = ['account_sid', 'twi_auth']


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Customer
        fields = ['id', 'agent', 'username', 'name', 'account_number', 'bank', 'location', 'digital_address', 'phone',
                  'date_of_birth', 'date_created']
        read_only_fields = ['agent']

    def get_username(self, user):
        username = user.agent.username
        return username


class AgentDepositRequestSerializer(serializers.ModelSerializer):
    guarantor_username = serializers.SerializerMethodField('get_guarantor_username')
    customer_username = serializers.SerializerMethodField('get_customer_username')
    agent_username = serializers.SerializerMethodField('get_agent_username')

    class Meta:
        model = AgentDepositRequests
        fields = ['id', 'guarantor', 'customer', 'agent', 'guarantor_username', 'customer_username', 'agent_username',
                  'amount', 'request_option', 'request_status', 'date_requested', 'time_requested']
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
        model = Payments
        fields = ['id', 'agent', 'agent_username', 'mode_of_payment', 'cash_at_location', 'amount',
                  'bank', 'reference', 'payment_action',
                  'payment_status', 'payment_for',
                  'date_created', 'time_created']
        read_only_fields = ['agent']

    def get_agent_username(self, user):
        agent_username = user.agent.username
        return agent_username


class AdminAccountsStartedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = AdminAccountsStartedWith
        fields = ['id', 'user', 'username', 'physical_cash', 'mtn_eCash', 'vodafone_eCash',
                  'airtel_tigo_eCash', 'ecobank_eCash',
                  'calbank_eCash', 'fidelity_eCash', 'ecash_sum', 'date_started']
        read_only_fields = ['user']

    def get_username(self, mm_user):
        username = mm_user.user.username
        return username


class AdminAccountsCompletedSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = AdminAccountsCompletedWith
        fields = ['id', 'user', 'username', 'physical_cash', 'mtn_eCash', 'vodafone_eCash',
                  'airtel_tigo_eCash', 'ecobank_eCash',
                  'calbank_eCash', 'fidelity_eCash', 'ecash_sum', 'date_closed']
        read_only_fields = ['user']

    def get_username(self, mm_user):
        username = mm_user.user.username
        return username
