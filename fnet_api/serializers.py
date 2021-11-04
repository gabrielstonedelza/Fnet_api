from rest_framework import serializers
from .models import FNetAdmin, Customer, AgentDepositRequests, CustomerWithdrawal, Payments


class FNetAdminSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = FNetAdmin
        fields = ['id', 'username']

    def get_username(self, user):
        username = user.user.username
        return username


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Customer
        fields = ['id', 'agent', 'username', 'name', 'account_number', 'bank', 'location', 'digital_address', 'phone',
                  'date_created']
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
                  'amount', 'bank', 'request_status', 'date_requested']
        read_only_fields = ['agent']

    def get_guarantor_username(self, user):
        guarantor_username = user.guarantor.user.username
        return guarantor_username

    def get_customer_username(self, user):
        customer_username = user.customer.name
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
        customer_username = user.customer.name
        return customer_username

    def get_agent_username(self, user):
        agent_username = user.agent.username
        return agent_username


class PaymentsSerializer(serializers.ModelSerializer):
    agent_username = serializers.SerializerMethodField('get_agent_username')

    class Meta:
        model = Payments
        fields = ['id', 'agent', 'agent_username', 'mode_of_payment', 'cash_at_location', 'amount', 'payment_status', 'date_created']
        read_only_fields = ['agent']

    def get_agent_username(self, user):
        agent_username = user.agent.username
        return agent_username
