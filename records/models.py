from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sauna_name = models.CharField(max_length=100)
    
    sauna_time = models.IntegerField(default=10)
    water_time = models.IntegerField(default=60)
    rest_time = models.IntegerField(default=10)
    
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # スコアを格納するフィールド
    apocalypse_score = models.IntegerField(default=0)

    # ▼▼▼ ここから追加：保存時にスコアを自動計算する魔法 ▼▼▼
    def save(self, *args, **kwargs):
        # 独自の計算式（例：サウナ1分=10点、水風呂10秒=10点、休憩1分=5点）
        # 数値を調整したい場合はここを書き換えてください
        score = (self.sauna_time * 10) + (self.water_time // 1) + (self.rest_time * 5)
        
        # 計算結果をフィールドに代入
        self.apocalypse_score = score
        
        # 本来の保存処理を実行
        super().save(*args, **kwargs)
    # ▲▲▲ ここまで追加 ▲▲▲

    def __str__(self):
        return f"{self.sauna_name} - {self.created_at}"