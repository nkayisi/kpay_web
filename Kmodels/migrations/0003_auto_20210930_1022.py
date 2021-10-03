# Generated by Django 3.2.7 on 2021-09-30 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kmodels', '0002_auto_20210930_0851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='type',
        ),
        migrations.AddField(
            model_name='transaction',
            name='desc_type',
            field=models.CharField(default='Envoie', max_length=250, verbose_name='Type ou description de la transaction'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='trans_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Coût de la transaction'),
        ),
        migrations.DeleteModel(
            name='Type',
        ),
    ]
