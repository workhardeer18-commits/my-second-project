from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView

from .forms import TicketForm, UserRegistrationForm
from .models import User, Ticket, Conversation


# --- Mixins ---
class AdminRequiredMixin(UserPassesTestMixin):
    login_url = "login"

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_superuser or getattr(user, 'user_type', '') == "admin")


# --- Views ---

class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')
            return render(request, self.template_name)


class RegisterView(TemplateView):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            # گرفتن داده‌های تایید شده از فرم
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # پسورد رو هش (Hash) کن
            user.save()

            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد')
            return redirect('index')
        else:
            # اگر فرم خطا داشت (مثلاً نام کاربری تکراری بود)
            messages.error(request, 'لطفاً فرم را به درستی پر کنید.')
            return render(request, self.template_name, {'form': form})


class HomeView(TemplateView):
    template_name = 'home.html'


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = 'index.html'

    def get_queryset(self):
        # این متد در TemplateView کاربرد مستقیم ندارد اما اگر در قالب استفاده می‌کنید لازم است
        user = self.request.user
        if user.user_type == 'admin' or user.is_superuser or user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)


# این کلاس را از داخل IndexView بیرون آوردم و اصلاح کردم
class CoversationRender(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'conversation_render.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin' or user.is_superuser or user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)


class CreateConversation(AdminRequiredMixin, View):
    template_name = 'CreateConversation.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        ticket_id = request.POST.get('ticket')
        message = request.POST.get('message')

        if not ticket_id or not message:
            messages.error(request, "داده‌های وارد شده معتبر نیستند")
            return redirect('create_conversation')

        ticket = get_object_or_404(Ticket, id=ticket_id)

        Conversation.objects.create(
            ticket=ticket,
            message=message,
            sender=request.user,
        )

        messages.success(request, "پیام با موفقیت ارسال شد")
        return redirect('ticket_detail', pk=ticket.id)


class Create_Ticket(LoginRequiredMixin, View):
    template_name = 'create_ticket.html'

    def get(self, request):
        form = TicketForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            if ticket.text:
                Conversation.objects.create(
                    ticket=ticket,
                    message=ticket.text,
                    sender=request.user,
                )
            messages.success(request, "تیکت با موفقیت ایجاد شد")
            return redirect('index')

        messages.error(request, "خطا در ثبت تیکت")
        return redirect('create_ticket')


class TicketDetails(LoginRequiredMixin, View):
    template_name = 'ticket_detail.html'

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        is_admin = request.user.user_type == 'admin' or request.user.is_superuser or request.user.is_staff
        is_owner = ticket.user == request.user

        if not (is_admin or is_owner):
            messages.error(request, "شما اجازه دسترسی به این تیکت را ندارید")
            return redirect('index')

        conversations = ticket.conversations.order_by('created_at')
        return render(request, self.template_name, {
            'ticket': ticket,
            'conversations': conversations
        })

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        is_admin = request.user.user_type == 'admin' or request.user.is_superuser or request.user.is_staff
        is_owner = ticket.user == request.user

        if not (is_admin or is_owner):
            messages.error(request, "شما اجازه ارسال پیام ندارید")
            return redirect('index')

        message = request.POST.get('message')
        if not message or not message.strip():
            messages.error(request, "متن پیام نمی‌تواند خالی باشد")
            return redirect('ticket_detail', pk=pk)

        Conversation.objects.create(
            ticket=ticket,
            message=message,
            sender=request.user,
        )
        messages.success(request, "پیام شما ارسال شد")
        return redirect('ticket_detail', pk=pk)
