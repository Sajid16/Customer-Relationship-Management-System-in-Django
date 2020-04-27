from accounts.models import *

# class Order:
#     def __init__(self):
#         pass
#
#     def all_order(self):
#         return Order.objects.all()

def all_order():
    return Order.objects.all()

def updateOrder(id):
    updateOrderInfo = Order.objects.get(id=id)
    return updateOrderInfo

def deleteOrder(id):
    deleteOrderInfo = Order.objects.get(id=id)
    return deleteOrderInfo

def total_orders_delivered():
    return Order.objects.filter(status='Delivered').count()

def total_orders_pending():
    return Order.objects.filter(status='Pending').count()

def specificCustomer(pk):
    individualCustomer = Customer.objects.get(id=pk)
    # print("value of ind customer: ",individualCustomer)
    individualTotalOrder = individualCustomer.order_set.count()
    individualOrderDetails = individualCustomer.order_set.all()
    return individualCustomer, individualTotalOrder, individualOrderDetails
