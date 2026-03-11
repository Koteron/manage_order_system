"""
Celery Task Definitions for Order Processing.

This module contains the actual implementation of background tasks 
triggered by the Kafka Consumer or the API. These tasks run in 
dedicated worker processes to ensure high availability of the web layer.
"""
import time
from app.celery.celery_worker import celery_app

@celery_app.task(name="tasks.process_order")
def process_order(order_id: int):
    """
    Simulates the background processing of a confirmed order.

    This function is executed by a Celery worker. In a production 
    environment, this would involve inventory updates, payment 
    finalization, or third-party API calls (e.g., shipping providers).

    Args:
        order_id: The unique identifier of the order to be processed.

    Note:
        The task name 'tasks.process_order' is the unique identifier 
        used by 'celery_client.send_task' to route the message 
        to this specific function.
    """
    time.sleep(2)
    print(f"Order {order_id} processed")