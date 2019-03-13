from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import ItemForm
from .models import NewUser, Item, SubCategory
from BackyardSale.views import updateTransactionItems


# Create your views here.


class dashboard(generic.DetailView):
    model = NewUser
    context_object_name = 'CurrentUser'
    template_name = 'DashBoard/dashboard.html'

    # Slug Field no longer needed, so Removed #

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super(dashboard, self).get_context_data(**kwargs)
        updateTransactionItems()
        context['ItemsListed'] = Item.objects.filter(Seller=self.request.user, CurrentStatus__range=[0,1]) # Check for range #
        context['ItemsSold'] = Item.objects.filter(Seller=self.request.user, CurrentStatus=2)
        context['ItemsRented'] = Item.objects.filter(Seller=self.request.user, CurrentStatus=3)
        context['RentedItemsbyMe'] = Item.objects.filter(RenterInfo=self.request.user, CurrentStatus=3)
        context['BoughtItems'] = Item.objects.filter(RenterInfo=self.request.user, CurrentStatus=2)

        return context


class createItem(generic.CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'DashBoard/createItem.html'
    success_url = reverse_lazy('Dashboard:dashboard')

    def form_valid(self, form):
        form.getCurrStatus()
        form.getSeller()
        return super(createItem, self).form_valid(form)

    def get_form_kwargs(self):
        kw = super(createItem, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw


def getSubCategories(request):
    cat_id = request.GET.get('Category')
    if cat_id == "":
        SubCategories = SubCategory.objects.none()
    else:
        SubCategories = SubCategory.objects.filter(ParentCategory_id=cat_id)

    return render(request, 'DashBoard/categoryDropdown.html', {"SubCategories": SubCategories})


class deleteItems(generic.DeleteView):
    model = Item
    success_url = reverse_lazy('Dashboard:dashboard')


class updateItems(generic.UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'DashBoard/createItem.html'
    success_url = reverse_lazy('Dashboard:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.getCurrStatus()
        form.getSeller()
        return super(updateItems, self).form_valid(form)

    def get_form_kwargs(self):
        kw = super(updateItems, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw


class approveView(generic.ListView):
    template_name = 'DashBoard/pendingTransactions.html'
    context_object_name = 'Items'

    def get_queryset(self):
        return Item.objects.filter(CurrentStatus__range=[4,6], Seller=self.request.user)
        #return Item.objects.all()

def approveItem(request, slug, pk):
    pass





