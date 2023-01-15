from django.shortcuts import render
from django.shortcuts import get_object_or_404
from listings.choices import bedroom_choices, price_choices, state_choices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from listings.models import Listing
# Create your views here.
def listings(request):
    listings=Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator= Paginator(listings,3)
    page=request.GET.get('page')
    paged_listings= paginator.get_page(page)
    context={
        'Listings': paged_listings

    }
    
    return render(request,'listings/listings.html',context)

def listing(request, listing_id):
    listing= get_object_or_404(Listing,pk=listing_id)
    context={
        'listing': listing
    }
    return render(request,'listings/listing.html',context)

def search(request):
    queryset_list=Listing.objects.order_by('-list_date')
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list=queryset_list.filter(description__icontains=keywords) #whole para
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list=queryset_list.filter(city__iexact=city)
    
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if city:
            queryset_list=queryset_list.filter(city__iexact=bedrooms)
    if 'price' in request.GET:
        price = request.GET['price']
        if city:
            queryset_list=queryset_list.filter(city__lte=price)

    context={
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request,'listings/search.html',context)