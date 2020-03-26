from django import forms
from .models import Blog
from django.utils.safestring import mark_safe

LOCATION_CHOICES = ( 
   ('BK', 'BROOKLYN'), 
   ('QS', 'QUEENS'), 
   ('MT', 'MANHATTAN'), 
   ('SI', 'STATE ISLAND'), 
) 


class HorizontalRadioRenderer(forms.RadioSelect):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class BlogPostForm(forms.ModelForm):
	class Meta:
		model=Blog
		fields = ['status', 'location', 'title', 'description','contact']
		labels={
			"status": "Status",
		}
		# status = forms.ChoiceField(choices=LOCATION_CHOICES, widget=forms.RadioSelect())
		widgets = {'status': forms.RadioSelect(attrs={'class': 'radiobuttons'}),
		'location': forms.RadioSelect(attrs={'class': 'radiobuttons'})}

