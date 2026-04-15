from django.db import migrations, models


def forwards_status_values(apps, schema_editor):
    Enrollment = apps.get_model("employee", "Enrollment")
    Enrollment.objects.filter(status="Enrolled").update(status="ENROLLED")
    Enrollment.objects.filter(status="Completed").update(status="COMPLETED")
    Enrollment.objects.filter(status="Cancelled").update(status="CANCELLED")


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards_status_values, noop_reverse),
        migrations.AlterField(
            model_name="enrollment",
            name="status",
            field=models.CharField(
                choices=[
                    ("ENROLLED", "ENROLLED"),
                    ("COMPLETED", "COMPLETED"),
                    ("CANCELLED", "CANCELLED"),
                ],
                default="ENROLLED",
                max_length=20,
            ),
        ),
    ]
