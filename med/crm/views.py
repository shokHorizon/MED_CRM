from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from . import forms, models

User = get_user_model()


def is_member(user):
    return user.groups.filter(name='clients').exists()


def index(request):
    if request.user:
        if request.user.is_staff:
            context = {'clinics': {}}
            for user in User.objects.all():
                if is_member(user):
                    context['clinics'][user.username] = user.first_name
            
            return render(request, 'index.html', context)
        
        return redirect(f'{request.user.username}/')

def clinic(request, pk):
    context = {}
    
    return render(request, 'clinic.html', context)

def storage(request, pk):
    if request.method == 'POST':
        form = forms.ItemForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            
    if request.GET.get('method', '') == 'delete':
        res = request.GET.get('name', '')
        if res:
            models.Item.objects.filter(name=res).delete()
            
    if request.GET.get('method', '') == 'edit':
        res_name = request.GET.get('name', '')
        res_amount = request.GET.get('amount', '')
        if res_name and res_amount:
            item = models.Item.objects.filter(name=res_name)
            if item.exists:
                item = item.first()
                item.amount = res_amount
                item.save()
    
    user = User.objects.get(username=pk)
    
    form = forms.ItemForm(initial={'clinic': user, 'used_today': 0})
    
    context = {
        'form': form,
        'clinic': pk,
    }
    
    items = models.Item.objects.filter(clinic=user)
    
    if items.exists():
        context['items'] = items.all()
        
    
    return render(request, 'storage.html', context)

def tasks(request, pk):
    
    if request.method == 'POST':
        form = forms.TaskForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            
    if request.GET.get('method', '') == 'delete':
        res = request.GET.get('name', '')
        if res:
            models.Task.objects.filter(name=res).delete()
    elif request.GET.get('method', '') == 'complete':
        res = request.GET.get('name', '')
        if res:
            task = models.Task.objects.filter(name=res).first()
            task.made = True
            task.save()
    
    user = User.objects.get(username=pk)
    
    form = forms.TaskForm(initial={'clinic': user, 'made': False})
    
    context = {
        'form': form,
        'clinic': pk,
    }
    
    tasks = models.Task.objects.filter(clinic=user)
    
    if tasks.exists():
        context['tasks'] = tasks.all()
        
    
    return render(request, 'tasks.html', context)

def partners(request, pk):
    
    if request.method == 'POST':
        form = forms.PartnerForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            
    if request.GET.get('method', '') == 'delete':
        res = request.GET.get('id', '')
        if res:
            models.Partner.objects.filter(id=res).delete()
            
    
    user = User.objects.get(username=pk)
    
    form = forms.PartnerForm(initial={'clinic': user})
    
    context = {
        'form': form,
    }
    
    clinic_partners = models.Partner.objects.filter(clinic=user)
    if clinic_partners.exists():
        context['partners'] = clinic_partners.all()
    
    return render(request, 'partners.html', context)

def clients(request, pk, id):
    
    if request.method == 'POST':
        form = forms.ClientForm(request.POST)
        print(form.errors)
        if form.is_valid():
            partner = models.Partner.objects.filter(id=id).first()
            partner.client_num += 1
            partner.save()
            form.save()
            
    if request.GET.get('method', '') == 'delete':
        res = request.GET.get('id', '')
        if res:
            client = models.Client.objects.filter(id=res)
            partner = models.Partner.objects.filter(id=id).first()
            partner.client_num -= 1
            partner.bill -= client.bill
            partner.payed -= client.payed
            partner.save()
            client.delete()
            
    if request.GET.get('method', '') == 'edit':
        res_id = request.GET.get('client_id', '')
        res_bill = request.GET.get('bill', '')
        res_payed = request.GET.get('payed', '')
        if res_id:
            client = models.Client.objects.filter(id=res_id)
            if client.exists:
                client = client.first()
                partner = models.Partner.objects.filter(id=id).first()
                if res_bill:
                    diff = client.bill - int(res_bill)
                    partner.bill -= diff
                    partner.save()
                    client.bill = res_bill
                if res_payed:
                    diff = client.payed - int(res_payed)
                    partner.payed -= diff
                    partner.save()
                    client.payed = res_payed
                client.save()
    
    form = forms.ClientForm(initial={'partner': id})
    
    context = {
        'form': form,
    }
    
    partner_clients = models.Client.objects.filter(partner=id)
    if partner_clients.exists():
        context['clients'] = partner_clients.all()
    
    return render(request, 'clients.html', context)
