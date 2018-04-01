# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from vendors import Vendors
import boto3
# Create your views here.


@api_view(['GET'])
def get_notifications(request):
    if request.method == "POST":
        return Response({"message":"Bad Request"}, status = status.HTTP_400_BAD_REQUEST)
    else:
        request_data  = request.data
        return Response({"message": request_data})


@api_view(['POST'])
def set_notifications(request):
    if request.method == "GET":
        return Response({"message":"Bad Request"}, status = status.HTTP_400_BAD_REQUEST)
    else:
        request_data  = request.data
        vendor_type = request_data["type"]
        
        # insert entry to sqs queue
        try:
            sqs = boto3.client('sqs')
        except Exception as exc:
            # raise Exception(str(exc))
            return Response({"message":"Internal Server Error Occurred"}. status.HTTP_500_INTERNAL_SERVER_ERROR)

        queue_url = 'SQS_QUEUE_URL'

        try:
            sqs_response = sqs.send_message(
                            QueueUrl=queue_url,
                            DelaySeconds=10,
                            MessageAttributes={
                                'Title': {
                                    'DataType': 'String',
                                    'StringValue': 'The Whistler'
                                },
                                'Author': {
                                    'DataType': 'String',
                                    'StringValue': 'John Grisham'
                                },
                                'WeeksOn': {
                                    'DataType': 'Number',
                                    'StringValue': '6'
                                }
                            },
                            MessageBody=(
                                'Information about current NY Times fiction bestseller for '
                                'week of 12/11/2016.'
                            )
                        )
        except Exception as exc:
            # raise Exception(str(exc))
            return Response({"message":"Internal Server Occured"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            sqs_response['MessageId']
        except Exception as exc:
            return Response({"message":"Internal Server Occured"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": response['MessageId']}, status.HTTP_201_CREATED)

