from django_cron import CronJobBase, Schedule
from django.utils import timezone
from .models import MatchM


class SetMatchToLiveCronJob(CronJobBase):
    # */5 * * * * /path/to/your/venv/bin/python /path/to/your/project/manage.py runcrons >> /tmp/cron.log 2>&1
    """
    Cron job to set matches to live status.
    Runs every minute.
    """
    RUN_EVERY_MINS = 1  # Run every minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'data.set_match_to_live_cron_job'  # Unique identifier for the cron job

    def do(self):
        now = timezone.now()
        matches = MatchM.objects.filter(status='SCHEDULED', date__lte=now)

        for match in matches:
            match.status = 'LIVE'
            match.save()
            print(f"Match {match.id} set to LIVE status.")


class UpdateStandingsCronJob(CronJobBase):
    """
    Cron job to update standings.
    Runs every hour.
    """
    RUN_EVERY_HOUR = 60  # Run every hour

    schedule = Schedule(run_every_mins=RUN_EVERY_HOUR)
    code = 'data.update_standings_cron_job'  # Unique identifier for the cron job

    def do(self):
        from data.management.commands.update_standings import Command
        command = Command()
        command.handle()
        print("Standings updated successfully.")