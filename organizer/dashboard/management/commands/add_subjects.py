from django.core.management.base import BaseCommand, CommandError
from dashboard.models import Subject

SUBJECTS = {
    "Vue.js",
    "Alpine.js",
    "React",
    "Angular",
    "Svelte",
    "JavaScript",
    "TypeScript",
    "Node.js",
    "Python",
    "Django",
    "Flask",
    "FastAPI",
    "Pyramid",
    "TailwindCSS",
    "Web Design",
    "Graphic Design",
    "UI/UX Design",
    "Ruby",
    "Ruby on Rails",
    "PHP",
    "Docker",
    "HTML",
    "CSS",
    "Twitter",
    "Facebook Ads",
    "SEO",
    "Laravel",
    "Bootstrap",
    "Swift",
    "SwiftUI",
    "GoLang",
    "WebFlow",
    "Wordpress",
    "Shopify",
    "Test Driven Development",
    "AWS",
    "Azure",
}


class Command(BaseCommand):
    help = 'Creates starting subjects'

    def handle(self, *args, **options):
        for subject in SUBJECTS:
            Subject.objects.create(name=subject)

        self.stdout.write(self.style.SUCCESS('Successfully created subjects'))
