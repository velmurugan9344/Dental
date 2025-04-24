from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages



from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm

# User Registration View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')  

    form = RegisterForm(request.POST or None)  
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check the form.")

    return render(request, 'register.html', {'form': form})

# User Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  

    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next', 'home')  

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect(next_url)  
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)
    request.session.flush()
    request.session.clear_expired()
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.conf import settings

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not found!")
            return redirect('login')  # Redirect back to login if email doesn't exist

        # Generate password reset token and UID
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        # Create reset link
        reset_link = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"

        # Render the email template with the reset link
        email_subject = "Password Reset Request"
        email_body = render_to_string('registration/password_reset_email.html', {
            'reset_link': reset_link,
            'user': user
        })

        # Send the email
        send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [email])

        messages.success(request, "A password reset link has been sent to your email.")
        return redirect('login')

    return render(request, 'login.html')  # Fallback render

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    selected_service = request.GET.get('service', '')
    selected_doctor = request.GET.get('doctor', '')
    return render(request, 'home.html', {
        'selected_service': selected_service,
        'selected_doctor': selected_doctor,
    })

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def price(request):
    return render(request,'price.html')

def appointment(request):
    return render(request,'appointment.html')

def testimonial(request):
    return render(request,'testimonial.html')

def service(request):
    return render(request,'service.html')

def team(request):
    return render(request,'team.html')

def testimonial(request):
    return render(request,'testimonial.html')

def terms(request):
    return render(request,'terms.html')

def privacy(request):
    return render(request,'privacy.html')

def search_not_found(request):
    return render(request, 'search_not_found.html')


# views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from .models import Appointment

def make_appointment(request):
    success_message = ""
    selected_service = request.GET.get('service', '')  # 💡 Get service from URL (GET)

    if request.method == 'POST':
        service = request.POST.get('service')
        doctor = request.POST.get('doctor')
        name = request.POST.get('name')
        email = request.POST.get('email')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        try:
            appointment_date = datetime.strptime(date_str, '%m/%d/%Y').date()
            appointment_time = datetime.strptime(time_str, '%I:%M %p').time()
        except ValueError:
            return render(request, 'appointment.html', {
                'success_message': '',
                'error_message': 'Invalid date format. Please select a valid date.',
                'selected_service': service  # Show selected again
            })

        appointment = Appointment.objects.create(
            service=service,
            doctor=doctor,
            name=name,
            email=email,
            date=appointment_date,
            time=appointment_time
        )

        cancel_url = request.build_absolute_uri(
            reverse('cancel_appointment', args=[appointment.id])
        )

        subject = 'Appointment Confirmation'
        message = f"Hi {name},\n\nYour appointment is confirmed on {appointment_date} at {appointment_time} with {doctor} for {service} treatment.\n\n" \
                  f"If you want to cancel, click here: {cancel_url}\n\nThanks!"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

        success_message = "Your appointment has been successfully submitted. A confirmation email has been sent."

        return render(request, 'appointment.html', {
            'success_message': success_message
        })

    # Render appointment page for GET (with prefilled service if passed)
    return render(request, 'appointment.html', {
        'selected_service': selected_service
    })

    



from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from .models import Appointment  # adjust import based on your project structure

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if not appointment.is_cancelled:
        appointment.is_cancelled = True
        appointment.save()

        # Email details
        subject = "Appointment Cancellation Confirmation"
        message = f"Hi {appointment.name},\n\nYour appointment for {appointment.service} with {appointment.doctor} " \
                  f"on {appointment.date} at {appointment.time.strftime('%I:%M %p')} has been successfully cancelled.\n\nThanks!"
        
        send_mail(subject, message, settings.EMAIL_HOST_USER, [appointment.email])

        message = "Your appointment has been successfully cancelled and a confirmation email has been sent."
    else:
        message = "This appointment was already cancelled."

    return render(request, 'cancel_status.html', {'message': message})

from django.shortcuts import render
from .models import Contact

def contact_view(request):
    success = ""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        success = "Your message has been sent successfully."

    return render(request, 'contact.html', {'success': success})


from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscriber

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Save email if not already subscribed
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            
            # Send confirmation email
            subject = 'Subscription Confirmed'
            message = 'Thank you for subscribing to our newsletter!'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


def search_doctors(request):
    service = request.GET.get('service', '').lower()

    doctors = [
        {
            "name": "Dr. Rajeev Khanna",
            "specialty": "Root Canal",
            "image": "img/team-1.jpg"
        },
        {
            "name": "Dr. Priya Mehra",
            "specialty": "Cosmetic Dentist",
            "image": "img/team-2.jpg"
        },
        {
            "name": "Dr. Arvind Patel",
            "specialty": "Dental Implant",
            "image": "img/team-3.jpg"
        },
        {
            "name": "Dr. Anjali Deshpande",
            "specialty": "Teeth Whitening",
            "image": "img/team-4.jpg"
        },
        {
            "name": "Dr. Sameer Reddy",
            "specialty": "Bridges Dentist",
            "image": "img/team-5.jpg"
        },
    ]

    matched_doctors = [doc for doc in doctors if service in doc['specialty'].lower()]

    context = {
        "doctors": matched_doctors,
        "selected_service": service.title()
    }
    return render(request, "search_results.html", context)



