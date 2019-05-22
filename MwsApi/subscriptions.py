# coding: utf-8
from MwsApi.mws_client import MwsClient


class Subscriptions(MwsClient):
    """
    订阅亚马逊推送接口
    """

    VERSION = '2013-07-01'
    URI = '/Subscriptions/{}'.format(VERSION)

    def register_destination(self, params):
        http_method = 'POST'
        action = 'RegisterDestination'

        dest = params.get('Destination')
        parameters = '&Destination.DeliveryChannel=SQS' + \
                     '&Destination.AttributeList.member.1.Key=sqsQueueUrl' + \
                     '&Destination.AttributeList.member.1.Value=' + dest
        return self.req_handler(http_method, action, parameters)

    def send_test_notification_to_destination(self, params):
        http_method = 'POST'
        action = 'SendTestNotificationToDestination'

        dest = params.get('Destination')
        parameters = '&Destination.DeliveryChannel=SQS' + \
                     '&Destination.AttributeList.member.1.Key=sqsQueueUrl' + \
                     '&Destination.AttributeList.member.1.Value=' + dest
        return self.req_handler(http_method, action, parameters)

    def create_subscription(self, params):
        http_method = 'POST'
        action = 'CreateSubscription'

        dest = params.get('Subscription').get('Destination')
        subscript_type = params.get('Subscription').get('NotificationType')
        parameters = '&Subscription.Destination.DeliveryChannel=SQS' + \
                     '&Subscription.Destination.AttributeList.member.1.Key=sqsQueueUrl' + \
                     '&Subscription.Destination.AttributeList.member.1.Value=' + dest + \
                     '&Subscription.IsEnabled=true' + \
                     '&Subscription.NotificationType=' + subscript_type
        return self.req_handler(http_method, action, parameters)

    def get_subscription(self, params):
        http_method = 'POST'
        action = 'GetSubscription'

        notification_type = params.get('NotificationType')
        dest = params.get('Destination')
        parameters = '&Destination.DeliveryChannel=SQS' + \
                     '&Destination.AttributeList.member.1.Key=sqsQueueUrl' + \
                     '&Destination.AttributeList.member.1.Value=' + dest + \
                     '&NotificationType=' + notification_type
        return self.req_handler(http_method, action, parameters)


    def req_handler(self, http_method, action, params):
        query_string = self.get_query_string(action, params, self.VERSION)
        signature = self.string_to_sign(http_method, self.URI, query_string)
        url = self.get_url(self.host, self.URI, query_string, signature)
        return self.excute_req(url, http_method)
