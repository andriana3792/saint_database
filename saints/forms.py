from django import forms
from django.forms import inlineformset_factory
from .models import (
    Saint,
    HagiographyOrWrittenSource,
    AspectsOfCult,
    ArchaeologicalAndArchitecturalEvidence,
    Image,
    Bibliography
)




class SaintForm(forms.ModelForm):
    feast_day = MonthDayField(
        required=False,
        help_text="Format: MM-DD (e.g., 12-25 for December 25)"
    )
    secondary_feast_date = MonthDayField(
        required=False,
        help_text="Format: MM-DD (e.g., 01-19 for January 19)"
    )

    class Meta:
        model = Saint
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'type_of_saint': forms.Select(attrs={'class': 'form-control'}),
            'act_period': forms.Select(attrs={'class': 'form-control'}),
            'region_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'region_of_burial': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control'}),
            'death_date': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter a brief description of the saint'
            }),
        }

# Inline Formsets for Related Models
HagiographyFormSet = inlineformset_factory(
    Saint,
    HagiographyOrWrittenSource,
    fields='__all__',
    extra=1,
    widgets={
        'literary_source_type': forms.Select(attrs={'class': 'form-control'}),
        'date_or_century_of_source': forms.TextInput(attrs={'class': 'form-control'}),
        'title_literary_text': forms.TextInput(attrs={'class': 'form-control'}),
        'liturgical_texts_source_type': forms.Select(attrs={'class': 'form-control'}),
        'date_or_century_of_liturgical_source': forms.TextInput(attrs={'class': 'form-control'}),
        'title_liturgical_text': forms.TextInput(attrs={'class': 'form-control'}),
    }
)

CultAspectsFormSet = inlineformset_factory(
    Saint,
    AspectsOfCult,
    fields='__all__',
    extra=1,
    widgets={
        'cult_place': forms.TextInput(attrs={'class': 'form-control'}),
        'pilgrimage_site': forms.Select(attrs={'class': 'form-control'}),
        'status': forms.Select(attrs={'class': 'form-control'}),
        'activities_accompanying_cult': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe rituals, festivals, or activities'
        }),
        'relics_cult_related_objects': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe relics or objects'
        }),
        'miracles': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe miracles'
        }),
    }
)

ArchaeologicalFormSet = inlineformset_factory(
    Saint,
    ArchaeologicalAndArchitecturalEvidence,
    fields='__all__',
    extra=1,
    widgets={
        'cult_buildings': forms.Select(attrs={'class': 'form-control'}),
        'date': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Year or century'
        }),
        'current_condition': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe current condition'
        }),
        'location': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Enter location details'
        }),
    }
)

ImageFormSet = inlineformset_factory(
    Saint,
    Image,
    fields='__all__',
    extra=1,
    widgets={
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'material_technique': forms.Select(attrs={'class': 'form-control'}),
        'site_monument': forms.TextInput(attrs={'class': 'form-control'}),
        'date': forms.TextInput(attrs={'class': 'form-control'}),
        'century': forms.Select(attrs={'class': 'form-control'}),
        'location_of_portrait': forms.Select(attrs={'class': 'form-control'}),
        'location_description': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2
        }),
        'iconographic_type': forms.Select(attrs={'class': 'form-control'}),
        'inscription_text': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2
        }),
        'description': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        }),
    }
)

BibliographyFormSet = inlineformset_factory(
    Saint,
    Bibliography,
    fields='__all__',
    extra=1,
    widgets={
        'reference': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter full bibliographic reference'
        }),
        'author': forms.TextInput(attrs={'class': 'form-control'}),
        'publication_date': forms.TextInput(attrs={'class': 'form-control'}),
    }
)

class SaintTimelineForm(forms.ModelForm):
    class Meta:
        model = SaintTimeline
        fields = '__all__'
        widgets = {
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

# Filter Forms
class SaintFilterForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name...'
        })
    )
    type_of_saint = forms.ChoiceField(
        choices=Saint.SAINT_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    act_period = forms.ChoiceField(
        choices=Saint.ACT_PERIOD_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )