from django import forms


class LocationForm(forms.Form):
    state = forms.CharField(max_length=50)


class DistrictForm(forms.Form):
    district = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = None
