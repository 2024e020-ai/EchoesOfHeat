from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required # これが必要です
from django.db.models import Sum # レベル計算に必要です
import datetime
import random
import json

from .models import Record
from .forms import RecordForm

# ---------------------------------------------------------
# 1. トップページ（レベル計算・ランク機能付き）
# ---------------------------------------------------------
@login_required
def index(request):
    # 検索機能
    query = request.GET.get('query')
    if query:
        records = Record.objects.filter(
            user=request.user, 
            sauna_name__icontains=query
        ).order_by('-created_at')
    else:
        records = Record.objects.filter(user=request.user).order_by('-created_at')

    # --- レベル計算ロジック ---
    # 全レコードの apocalypse_score の合計を出す
    total_score = records.aggregate(Sum('apocalypse_score'))['apocalypse_score__sum'] or 0
    # 500点ごとに1レベルアップ
    user_level = total_score // 500  

    # 通算回数とランク判定
    total_count = records.count()
    if total_count <= 10:
        user_rank = "微熱を纏いし灰の旅人"
    elif total_count <= 50:
        user_rank = "煉獄の炎を御する執行者"
    else:
        user_rank = "蒸気世界を統べる絶対神"

    # グラフ用データの作成
    graph_dates = []
    graph_scores = []
    for r in records.order_by('created_at')[:10]: 
        graph_dates.append(r.created_at.strftime('%m/%d'))
        graph_scores.append(r.apocalypse_score)

    # ランダムな一言
    quotes = [
        "整いは一日にして成らず", 
        "熱こそが正義", 
        "水風呂は裏切らない",
        "サウナの熱は魂の熱",
        "静寂の中に答えはある"
    ]
    random_quote = random.choice(quotes)

    context = {
        'records': records,
        'total_count': total_count,
        'user_rank': user_rank,
        'user_level': user_level,    # これでレベルが渡るようになります
        'total_score': total_score,  # 合計点も渡します
        'random_quote': random_quote,
        'search_query': query,
        'graph_dates': json.dumps(graph_dates),
        'graph_scores': json.dumps(graph_scores),
    }
    return render(request, 'list.html', context)


# ---------------------------------------------------------
# 2. CRUD機能（クラスベースビュー）
# ---------------------------------------------------------

class RecordDetail(LoginRequiredMixin, generic.DetailView):
    model = Record
    template_name = 'detail.html'
    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)

class RecordCreate(LoginRequiredMixin, generic.CreateView):
    model = Record
    form_class = RecordForm
    template_name = 'form.html'
    success_url = reverse_lazy('list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecordUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Record
    form_class = RecordForm
    template_name = 'form.html'
    success_url = reverse_lazy('list')
    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)

class RecordDelete(LoginRequiredMixin, generic.DeleteView):
    model = Record
    template_name = 'delete.html'
    success_url = reverse_lazy('list')
    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)

# ---------------------------------------------------------
# 3. カレンダー機能
# ---------------------------------------------------------
class CalendarView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        records = Record.objects.filter(user=self.request.user)
        events = []
        for rec in records:
            events.append({
                'title': rec.sauna_name,
                'start': rec.created_at.strftime('%Y-%m-%d'),
                'url': f"/detail/{rec.pk}/"
            })
        context['events_json'] = json.dumps(events)
        return context

# ---------------------------------------------------------
# 4. 認証機能
# ---------------------------------------------------------
class Login(LoginView):
    template_name = 'auth/login.html'

class Logout(LogoutView):
    next_page = reverse_lazy('login')

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('list')
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('list')