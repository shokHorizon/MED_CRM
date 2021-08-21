from django import forms

from . import models


class TaskForm(forms.ModelForm):

	class Meta:
		model = models.Task
		fields = ['name', 'desc', 'made', 'clinic']
  
class ItemForm(forms.ModelForm):

	class Meta:
		model = models.Item
		fields = ['name', 'amount', 'used_today', 'clinic']
    
class PartnerForm(forms.ModelForm):

	class Meta:
		model = models.Partner
		fields = ['name', 'surname', 'clinic']
    
class ClientForm(forms.ModelForm):

	class Meta:
		model = models.Client
		fields = ['name', 'surname', 'isAdult', 'partner']
  