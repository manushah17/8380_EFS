from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


now = timezone.now()


def home(request):
    return render(request, 'portfolio/home.html', {'portfolio': home})


@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'portfolio/customer_list.html', {'customers': customer})

@login_required
def customer_edit(request, pk):
       customer = get_object_or_404(Customer, pk=pk)
       form = CustomerForm(request.POST or None)
       if request.method == "POST":
           # update
           form = CustomerForm(request.POST, instance=customer)
           if form.is_valid():
               customer = form.save(commit=False)
               customer.updated_date = timezone.now()
               customer.save()
               customer = Customer.objects.filter(created_date__lte=timezone.now())
               return render(request, 'portfolio/customer_list.html',
                             {'customers': customer})
       else:
            # edit
           form = CustomerForm(instance=customer)
       return render(request, 'portfolio/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
       customer = get_object_or_404(Customer, pk=pk)
       customer.delete()
       return redirect('portfolio:customer_list')


@login_required
def stock_list(request):
       stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
       return render(request, 'portfolio/stock_list.html', {'stocks': stocks})


@login_required
def stock_new(request):
       if request.method == "POST":
           form = StockForm(request.POST)
           if form.is_valid():
               stock = form.save(commit=False)
               stock.created_date = timezone.now()
               stock.save()
               stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
               return render(request, 'portfolio/stock_list.html',
                             {'stocks': stocks})
       else:
           form = StockForm()
           # print("Else")
       return render(request, 'portfolio/stock_new.html', {'form': form})


@login_required
def stock_edit(request, pk):
       stock = get_object_or_404(Stock, pk=pk)
       if request.method == "POST":
           form = StockForm(request.POST, instance=stock)
           if form.is_valid():
               stock = form.save()
               # stock.customer = stock.id
               stock.updated_date = timezone.now()
               stock.save()
               stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
               return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
           else:
               # print("else")
               form = StockForm(instance=stock)
           return render(request, 'portfolio/stock_edit.html', {'form': form})


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('portfolio:home')
    return render(request, 'registration/login_form.html', {'form': form, 'title': title})


def register_view(request):
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('portfolio:home')

    context = {
        "form": form,
        "title": title
    }
    return render(request, "registration/login_form.html", context)


def logout_view(request):
    logout(request)
    return redirect('portfolio:home')

