from django.urls import path
from . import views

urlpatterns = [
    # 1. トップページ（関数 views.index を呼び出すように修正）
    path('', views.index, name='list'),
    
    # 2. 詳細画面
    path('detail/<int:pk>/', views.RecordDetail.as_view(), name='detail'),
    
    # 3. 新規作成
    path('create/', views.RecordCreate.as_view(), name='create'),
    
    # 4. 編集（修正）
    path('update/<int:pk>/', views.RecordUpdate.as_view(), name='update'),
    
    # 5. 削除（抹消）
    path('delete/<int:pk>/', views.RecordDelete.as_view(), name='delete'),
    
    # 6. カレンダー（もし views.py で CalendarView クラスを定義している場合）
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    
    # 7. ログイン・ログアウト・登録
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('accounts/logout/', views.Logout.as_view(), name='logout'),
    path('accounts/signup/', views.SignUp.as_view(), name='signup'),
]