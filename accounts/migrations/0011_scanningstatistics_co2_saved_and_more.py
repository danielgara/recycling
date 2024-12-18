# Generated by Django 5.0 on 2024-11-24 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_scanningstatistics"),
    ]

    operations = [
        migrations.AddField(
            model_name="scanningstatistics",
            name="co2_saved",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="scanningstatistics",
            name="bin_type",
            field=models.CharField(
                choices=[
                    ("BLACK", "Negra - No Reciclable"),
                    ("GREEN", "Verde - Orgánicos"),
                    ("WHITE", "Blanca - Reciclables"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="scanningstatistics",
            name="waste_type",
            field=models.CharField(
                choices=[
                    ("BOTTLE", "Botella"),
                    ("PRINTED_PACKAGING", "Empaques Impresos"),
                    ("CONTAINER", "Envase"),
                    ("CAN", "Lata"),
                    ("ORGANIC", "Orgánico"),
                    ("OTHER", "Otros"),
                    ("NON_RECYCLABLE_PAPER", "Papel no reciclable"),
                    ("PAPERS", "Papeles"),
                    ("UNCERTAIN", "Incierto"),
                ],
                max_length=50,
            ),
        ),
    ]
