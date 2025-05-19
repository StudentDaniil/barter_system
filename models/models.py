from django.db import models
from django.conf import settings


class Advertisement(models.Model):
    """Модель объявления о товаре"""
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    title = models.CharField("Заголовок", max_length=200)
    description = models.TextField("Описание")
    image_url = models.URLField("URL изображения", blank=True, null=True)
    category = models.CharField("Категория", max_length=200)
    condition = models.CharField(
        "Состояние",
        max_length=10,
        choices=CONDITION_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_condition_display()})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        db_table = 'advertisement'


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name='sent_proposals',
        verbose_name="Объявление инициирующего предложение "
    )

    ad_receiver = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name='received_proposals',
        verbose_name="Объявление получателя"
    )

    comment = models.TextField(
        "Комментарий",
        blank=True,
        help_text="Дополнительная информация для получателя"
    )

    status = models.CharField(
        "Статус предложения",
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['ad_sender', 'ad_receiver'],
                name='unique_proposal'
            )
        ]
        db_table = 'exchangeProposal'

    def __str__(self):
        return f"#{self.id} {self.ad_sender.title} → {self.ad_receiver.title} ({self.get_status_display()})"
