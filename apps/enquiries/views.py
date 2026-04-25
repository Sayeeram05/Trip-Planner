from django.shortcuts import render, redirect, get_object_or_404
from .forms import EnquiryForm
from apps.packages.models import Package


def enquiry_create(request, package_id):
    package = get_object_or_404(Package, id=package_id, is_active=True)

    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.package = package
            enquiry.destination = package.title
            enquiry.save()
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
