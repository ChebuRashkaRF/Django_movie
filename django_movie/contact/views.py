from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm
from .service import send
from .tasks import send_spam_mail


class ContactView(CreateView):
    """Отображение формы подписки по email"""

    model = Contact
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        # send(form.instance.email)
        send_spam_mail.delay(form.instance.email)
        return super().form_valid(form)
