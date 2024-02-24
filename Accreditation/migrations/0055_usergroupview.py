# Generated by Django 5.0.1 on 2024-02-20 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accreditation', '0054_accreditation_certificates'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroupView',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=254)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('middle_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('profile_pic', models.CharField(max_length=100)),
                ('user_group', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'user_group_view',
                'managed': False,
            },
        ),

        migrations.RunSQL(
            """
            DROP VIEW IF EXISTS user_group_view;
            CREATE VIEW user_group_view 
                AS
                SELECT DISTINCT	u.id, 
                        u.profile_pic,
                        u.first_name, 
                        u.last_name,
                        u.middle_name,
                        u.email,
                       ARRAY( SELECT grp_1.name
                                FROM auth_group grp_1
                                JOIN "Users_customuser_groups" ug_1 
                                    ON grp_1.id = ug_1.group_id
                                JOIN "Users_customuser" u_1 
                                    ON u_1.id = ug_1.customuser_id
                                WHERE u_1.id = u.id) AS user_group
                        
                FROM public."Users_customuser" u
                INNER JOIN  public."Users_customuser_groups" ug
                ON u.id = ug.customuser_id
                INNER JOIN public."auth_group" grp
                ON grp.id = ug.group_id
                WHERE u.is_active = TRUE;
            """
        )
    ]