import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.template import engines

from .forms import EnquiryForm
from .models import EmailTemplate
from apps.packages.models import Package

logger = logging.getLogger(__name__)


def _send_enquiry_emails(enquiry):
    """Send admin notification + customer confirmation emails.
    Any failure is logged but never raises — it must not break the form flow.
    """
    context = {
        "full_name": enquiry.full_name,
        "email": enquiry.email,
        "phone": enquiry.phone,
        "location": enquiry.location,
        "destination": enquiry.destination,
        "travel_date": enquiry.travel_date.strftime("%d %B %Y"),
        "people_count": enquiry.people_count,
        "package": enquiry.package,
    }

    django_engine = engines["django"]

    try:
        admin_tpl = EmailTemplate.objects.get(name=EmailTemplate.ADMIN_NOTIFICATION)
        admin_subject = django_engine.from_string(admin_tpl.subject).render(context)
        admin_body = django_engine.from_string(admin_tpl.html_body).render(context)

        msg = EmailMultiAlternatives(
            subject=admin_subject,
            body=f"New enquiry from {enquiry.full_name} for {enquiry.destination}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_ENQUIRY_EMAIL],
        )
        msg.attach_alternative(admin_body, "text/html")
        msg.send(fail_silently=False)
    except Exception:
        logger.exception(
            "Failed to send admin notification email for enquiry id=%s", enquiry.pk
        )

    try:
        customer_tpl = EmailTemplate.objects.get(
            name=EmailTemplate.CUSTOMER_CONFIRMATION
        )
        customer_subject = django_engine.from_string(customer_tpl.subject).render(
            context
        )
        customer_body = django_engine.from_string(customer_tpl.html_body).render(
            context
        )

        msg = EmailMultiAlternatives(
            subject=customer_subject,
            body=(
                f"Hi {enquiry.full_name}, thank you for enquiring about "
                f"{enquiry.destination}. Our team will contact you within 24 hours."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[enquiry.email],
        )
        msg.attach_alternative(customer_body, "text/html")
        msg.send(fail_silently=False)
    except Exception:
        logger.exception(
            "Failed to send customer confirmation email for enquiry id=%s", enquiry.pk
        )


def enquiry_create(request, package_id):
    package = get_object_or_404(Package, id=package_id, is_active=True)

    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.package = package
            enquiry.destination = package.title
            enquiry.save()
            _send_enquiry_emails(enquiry)
            return redirect("enquiries:success")
    else:
        form = EnquiryForm(initial={"destination": package.title})

    return render(
        request,
        "enquiries/form.html",
        {
            "form": form,
            "package": package,
        },
    )


def enquiry_success(request):
    return render(request, "enquiries/success.html")
