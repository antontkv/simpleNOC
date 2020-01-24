from django.shortcuts import render, redirect
from IPAM.forms import SubnetsAddForm
from django.views.generic.edit import FormView
from IPAM import helpers as ipam_helpers

class AddSubnetsView(FormView):
    template_name = 'ipam/add_subnets.html'
    form_class = SubnetsAddForm
    success_url = '/ipam/add_subnets/summary/'

    def form_valid(self, form):
        add_subnets_result = ipam_helpers.add_multiple_subnets(
            form.cleaned_data['subnets_to_add']
        )
        self.request.session['valid_subnets'] = add_subnets_result[0]
        self.request.session['invalid_subnets'] = add_subnets_result[1]
        return super().form_valid(form)


def add_subnets_summary(request):
    valid_subnets = request.session.get('valid_subnets')
    invalid_subnets = request.session.get('invalid_subnets')

    if request.method == 'POST':
        if 'add_subnets' in request.POST:
            ipam_helpers.add_multiple_subnets('\r\n'.join(valid_subnets), True)
            return redirect('add-subnets')
        else:
            return redirect('add-subnets')

    return render(
        request,
        'ipam/add_subnets_summary.html',
        {'valid_subnets': valid_subnets, 'invalid_subnets': invalid_subnets}
    )
