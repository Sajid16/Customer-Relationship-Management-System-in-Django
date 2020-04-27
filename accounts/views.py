from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from accounts.models import *
from accounts import db_functions
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import OrderForm, CreateUserForm
from accounts.filters import orderFilter

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout # used in login and logout for authenticate nad its build-in
from django.contrib.auth.decorators import login_required
from accounts.decorators import *
from django.contrib.auth.models import Group

# Create your views here.

@unauthenticatedUser
def registerPage(request):

    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            # print('on line 21')
            user = form.save()
            # print('on line 23')
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.add_message(request, messages.SUCCESS, 'Account was created for ' + username)
            # messages.success(request, 'Account was created for ' + user)
            return redirect('login')

        else:
            context = {'form':form}
            return render(request, 'accounts/register.html', context)
    else:
        context = {'form':form}
        return render(request, 'accounts/register.html', context)


@unauthenticatedUser
def loginPage(request):
    # context = {}
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING, 'Username or Password is incorrect!')
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')


def logOutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowedUsers(allowed_roles=['customer'])
def userProfile(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@adminOnly
def home(request):

    # username = request.user.username
    customers = Customer.objects.all()
    # Order = db_functions.Order()
    orders = db_functions.all_order()
    total_orders = orders.count()
    orders_delivered = db_functions.total_orders_delivered()
    orders_pending = db_functions.total_orders_pending()
    context ={
        # 'username': username,
        'customers': customers,
        'orders': orders,
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,

    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowedUsers(allowed_roles=['admin'])
def products(request):

    context = {
        'products': Product.objects.all()
    }
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowedUsers(allowed_roles=['admin'])
def customer(request, pk):

    individualCustomer,individualTotalOrder,individualOrderDetails = db_functions.specificCustomer(pk)

    context = {
        'customer': individualCustomer,
        'totalOrder': individualTotalOrder,
        'orderDetails': individualOrderDetails,
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowedUsers(allowed_roles=['admin'])
def createOrder(request, pk):
    # customer = db_functions.specificCustomer(pk)
    # print(customer)
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        # form = OrderForm(request.POST)
        formSet = orderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('customer', pk=pk)
    else:
        # form = OrderForm(initial={'customer':customer})
        formSet = orderFormSet(queryset=Order.objects.none(), instance=customer)
        context ={
            'form': formSet,
        }
        return render(request, "accounts/order_form.html", context)


@login_required(login_url='login')
@allowedUsers(allowed_roles=['admin'])
def updateOrder(request, pk):
    updateOrder = db_functions.updateOrder(pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=updateOrder)
        if form.is_valid():
            form.save()
            # print("debug on line 69")
            return redirect('home')
    else:
        form = OrderForm(instance=updateOrder)
        context = {
            'form': form,
        }
        return  render(request, "accounts/order_form.html", context)


@login_required(login_url='login')
@allowedUsers(allowed_roles=['admin'])
def individualCustomerUpdateOrder(request, pk, customer_id):
    updateOrder = db_functions.updateOrder(pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=updateOrder)
        if form.is_valid():
            form.save()
            # print("debug on line 83")
            return redirect('customer', pk=customer_id)
    else:
        form = OrderForm(instance=updateOrder)
        context = {
            'form': form,
        }
        return  render(request, "accounts/order_form.html", context)


@login_required(login_url='login')
@allowedUsers(allowed_roles=['admin'])
def deleteOrder(request, pk):
    deleteOrder = db_functions.deleteOrder(pk)
    deleteOrder.delete()
    return redirect('home')


@login_required(login_url='login')
@allowedUsers(allowed_roles=['admin'])
def individualCustomerDeleteOrder(request, pk, customer_id):
    deleteOrder = db_functions.deleteOrder(pk)
    deleteOrder.delete()
    return redirect('customer', pk=customer_id)
