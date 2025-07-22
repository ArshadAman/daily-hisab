from django.db import models


from users.models import User, Business

class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')])
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='categories')
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.type})"

class IncomeExpense(models.Model):
    ENTRY_TYPE = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=ENTRY_TYPE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    payment_mode = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    voice_entry = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} - {self.amount}"
