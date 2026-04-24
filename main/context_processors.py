from django.conf import settings


def site_context(request):
    return {
        "STREAMLIT_URL": settings.STREAMLIT_URL,
    }
