from django.db import migrations

ADMIN_BODY = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
  .wrapper { max-width: 620px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,.1); }
  .header { background: #4e5b31; padding: 24px 32px; }
  .header h1 { color: #d4af37; margin: 0; font-size: 22px; }
  .header p { color: #c8d4a0; margin: 4px 0 0; font-size: 13px; }
  .body { padding: 28px 32px; }
  .body h2 { color: #4e5b31; font-size: 17px; margin: 0 0 18px; border-bottom: 2px solid #d4af37; padding-bottom: 8px; }
  table { width: 100%; border-collapse: collapse; }
  td { padding: 10px 12px; font-size: 14px; border-bottom: 1px solid #f0f0f0; vertical-align: top; }
  td:first-child { font-weight: 600; color: #555; width: 38%; }
  td:last-child { color: #222; }
  .footer { background: #f9f9f9; padding: 16px 32px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #eee; }
</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <h1>Sri Narpavi Holidays</h1>
    <p>New Enquiry Received</p>
  </div>
  <div class="body">
    <h2>Enquiry Details</h2>
    <table>
      <tr><td>Full Name</td><td>{{ full_name }}</td></tr>
      <tr><td>Email</td><td>{{ email }}</td></tr>
      <tr><td>Phone</td><td>{{ phone }}</td></tr>
      <tr><td>Location</td><td>{{ location }}</td></tr>
      <tr><td>Destination / Package</td><td>{{ destination }}</td></tr>
      <tr><td>Travel Date</td><td>{{ travel_date }}</td></tr>
      <tr><td>Number of People</td><td>{{ people_count }}</td></tr>
    </table>
  </div>
  <div class="footer">This notification was generated automatically by Sri Narpavi Holidays.</div>
</div>
</body>
</html>"""

CUSTOMER_BODY = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
  .wrapper { max-width: 620px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,.1); }
  .header { background: #4e5b31; padding: 24px 32px; }
  .header h1 { color: #d4af37; margin: 0; font-size: 22px; }
  .header p { color: #c8d4a0; margin: 4px 0 0; font-size: 13px; }
  .body { padding: 28px 32px; color: #333; line-height: 1.7; font-size: 15px; }
  .body h2 { color: #4e5b31; font-size: 19px; margin: 0 0 14px; }
  .highlight { background: #f7f3e8; border-left: 4px solid #d4af37; padding: 14px 18px; border-radius: 4px; margin: 20px 0; font-size: 14px; }
  .footer { background: #f9f9f9; padding: 16px 32px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #eee; }
</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <h1>Sri Narpavi Holidays</h1>
    <p>Your enquiry is confirmed!</p>
  </div>
  <div class="body">
    <h2>Thank you, {{ full_name }}!</h2>
    <p>We have received your enquiry for <strong>{{ destination }}</strong> and we're thrilled to help you plan your perfect trip.</p>
    <div class="highlight">
      <strong>What happens next?</strong><br>
      Our travel expert will review your details and reach out to you within <strong>24 hours</strong> at <strong>{{ phone }}</strong> or <strong>{{ email }}</strong>.
    </div>
    <p>Here's a summary of what you submitted:</p>
    <ul>
      <li><strong>Destination:</strong> {{ destination }}</li>
      <li><strong>Travel Date:</strong> {{ travel_date }}</li>
      <li><strong>Number of Travellers:</strong> {{ people_count }}</li>
    </ul>
    <p>If you have any urgent questions, feel free to reach us at <a href="mailto:mailforprogram01@gmail.com" style="color:#4e5b31;">mailforprogram01@gmail.com</a>.</p>
    <p>Warm regards,<br><strong>Sri Narpavi Holidays Team</strong></p>
  </div>
  <div class="footer">&copy; Sri Narpavi Holidays. All rights reserved.</div>
</div>
</body>
</html>"""


def seed_templates(apps, schema_editor):
    EmailTemplate = apps.get_model("enquiries", "EmailTemplate")
    EmailTemplate.objects.get_or_create(
        name="admin_notification",
        defaults={
            "subject": "New Enquiry: {{ destination }} — {{ full_name }}",
            "html_body": ADMIN_BODY,
        },
    )
    EmailTemplate.objects.get_or_create(
        name="customer_confirmation",
        defaults={
            "subject": "Thank you for your enquiry — Sri Narpavi Holidays",
            "html_body": CUSTOMER_BODY,
        },
    )


def unseed_templates(apps, schema_editor):
    EmailTemplate = apps.get_model("enquiries", "EmailTemplate")
    EmailTemplate.objects.filter(
        name__in=["admin_notification", "customer_confirmation"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("enquiries", "0002_emailtemplate"),
    ]

    operations = [
        migrations.RunPython(seed_templates, reverse_code=unseed_templates),
    ]
