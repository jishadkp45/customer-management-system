from django.shortcuts import render,redirect
from .models import *
from .forms import orderForm
from .filters import orderFilters



def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'orders': orders, 'customers': customers,'total_customers':total_customers,
    'total_orders':total_orders,'delivered':delivered,'pending':pending}

    return render(request, 'accounts/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products' :products})

def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    
    Filter = orderFilters(request.GET,queryset = orders)
    orders = Filter.qs
    context ={'customer' : customer,'orders':orders,'total_orders':total_orders,'Filter':Filter}

    return render(request, 'accounts/customer.html',context)

def createOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    form = orderForm(initial={'customer': customer})
    if request.method == 'POST':
        form = orderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    

    context ={'form':form}
    return render(request, 'accounts/create_order.html',context)


def updateOrder(request,pk):
    
    order = Order.objects.get (id = pk) 
    form = orderForm(instance=order)
    if request.method == 'POST':
        form = orderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
      
    context ={'form':form}
    return render(request, 'accounts/create_order.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get (id = pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    
    context ={'order':order}

    return render(request, 'accounts/delete.html',context)
