from django.contrib import admin
from django.urls import path

from main.views import LoginView, RegisterView, HomeView, IndexView, CoversationRender, CreateConversation, \
    Create_Ticket, TicketDetails

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),  # این خط را اضافه کنید تا آدرس اصلی به صفحه خانه وصل شود
    path('index/', IndexView.as_view(), name='index'),
    # سایر مسیرهای شما...
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('index/', IndexView.as_view(), name='index'),
    path('conversations/', CoversationRender.as_view(), name='conversation_render'),
    path('create-conversation/', CreateConversation.as_view(), name='create_conversation'),
    path('create-ticket/', Create_Ticket.as_view(), name='create_ticket'),
    path('ticket/<int:pk>/', TicketDetails.as_view(), name='ticket_detail'),
]
