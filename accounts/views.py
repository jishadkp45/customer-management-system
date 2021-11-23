from django.contrib.auth import authenticate
from django.forms.forms import Form
from django.forms import inlineformset_factory
from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm,CreateUserForm,customerForm
from .filters import orderFilters
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_users,admin_only

@unauthenticated_user
def loginPage(request):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username,password = password )
            
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                    messages.info(request,'username or password incorrect')
                    return render(request,'accounts/login.html')



        return render(request,'accounts/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
           
            messages.success(request,'account created succesfully for ' + username)

            return redirect('login')
          
    
    context = {'form':form}
    return render(request,'accounts/register.html',context)



@login_required( login_url='login')
@admin_only

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


@login_required( login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}

    return render(request,'accounts/user.html',context)


@login_required( login_url='login')
@allowed_users(allowed_roles=['customer'])
def accSettings(request):
    customer = request.user.customer
    form = customerForm(instance=customer)
    if request.method == 'POST':
        form = customerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request,'accounts/acc_settings.html',context)


@login_required( login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products' :products})



@login_required( login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    
    Filter = orderFilters(request.GET,queryset = orders)
    orders = Filter.qs
    context ={'customer' : customer,'orders':orders,'total_orders':total_orders,'Filter':Filter}

    return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status') )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	print('ORDER:', order)
	if request.method == 'POST':

		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_order.html', context)


@login_required( login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get (id = pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    
    context ={'order':order}

    return render(request, 'accounts/delete.html',context)
