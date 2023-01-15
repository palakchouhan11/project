from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from contacts.models import Contact

def contact(request):
    if request.method =='POST':
        listing_id=request.POST['listing_id']
        listing=request.POST['listing']
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        user_id=request.POST['user_id']
        realtor_email=request.POST['realtor_email']
        #check if inquiry already made
        if request.user.is_authenticated:
            user_id=request.user.id
            has_contacted=Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'you already made inquiry for this')
                return redirect('/listings/'+listing_id)
        contact=Contact(listing=listing, listing_id=listing_id,name=name,email=email,phone=phone, message=message,user_id=user_id)
        contact.save()
        # send mail
        send_mail(
            'propert listing inquiry',
            'there has been an inquiry for' + listing + '. sign into admin panel for more info',
            'palakchouhan113@gmail.com',
            [realtor_email,'chouhanpriya2001@gmail.com'],
            fail_silently=False

        )
        messages.success(request,'request submitted, a retalor will contact soon')
        return redirect('/listings/'+listing_id)