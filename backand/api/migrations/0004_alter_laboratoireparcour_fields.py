# Generated migration to fix NOT NULL constraint issues
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_candidatureparcours_competences_techniques_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratoireparcour',
            name='date_creation',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laboratoireparcour',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laboratoireparcour',
            name='duree_formation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laboratoireparcour',
            name='nombre_etudiant_max',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]