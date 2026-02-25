from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import json
import logging

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')


def contact(request):
    return render(request, 'contact.html')

# Create your views here.


def _kb_answer(text: str) -> str | None:
    t = text.lower()
    kb = [
        (['track', 'status'], "Track orders with your ID at /orders/track/."),
        (['hour', 'open', 'close'], "We bake daily 7am–7pm. Deliveries 9am–6pm."),
        (['deliver', 'shipping'], "Same-day delivery before 12pm. Free delivery over $50."),
        (['pickup', 'collect'], "Pickup is available; choose pickup at checkout."),
        (['custom', 'wedding', 'birthday'], "We create custom cakes. Typical lead time 48–72 hours."),
        (['flavor', 'menu'], "Popular flavors: vanilla, chocolate fudge, red velvet, lemon, carrot."),
        (['allergen', 'gluten', 'nut', 'vegan'], "Ask for allergen-friendly options. Traces may remain."),
        (['store', 'keep', 'fridge', 'freeze'], "Cakes keep 2 days refrigerated. Cupcakes best same day."),
        (['refund', 'cancel', 'return'], "Cancel up to 24h before delivery. Quality issues: contact us within 24h."),
        (['contact', 'email', 'phone'], "Use the Contact page or email hello@sweetcrumbs.test."),
        (['cupcakes'], "Browse cupcakes at /shop?c=cupcakes"),
        (['cookies'], "Browse cookies at /shop?c=cookies"),
        (['wedding'], "Browse wedding cakes at /shop?c=wedding"),
        (['birthday'], "Browse birthday cakes at /shop?c=birthday"),
    ]
    for keys, answer in kb:
        if any(k in t for k in keys):
            return answer
    return None


def _openai_answer(prompt: str) -> str | None:
    api_key = getattr(settings, 'OPENAI_API_KEY', None)
    if not api_key:
        return None
    try:
        # Lazy import so package is optional
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        system = (
            "You are a helpful bakery assistant for Sweet Crumbs Bakery. "
            "Answer clearly and concisely about products, orders, delivery, custom cakes, allergens, store hours."
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=250,
        )
        return (resp.choices[0].message.content or '').strip()
    except Exception as e:
        logger.exception("OpenAI chat failed: %s", e)
        return None


@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    message = (data.get('message') or '').strip()
    if not message:
        return JsonResponse({"error": "Empty message"}, status=400)

    # Try LLM first if configured, then fallback to KB
    # Check if LLM is enabled
    llm_enabled = True
    try:
        from .models import SiteConfig
        cfg = SiteConfig.objects.first()
        if cfg is not None:
            llm_enabled = bool(cfg.llm_enabled)
    except Exception:
        llm_enabled = True

    answer = _openai_answer(message) if llm_enabled else None
    if not answer:
        answer = _kb_answer(message)

    if answer:
        return JsonResponse({"answer": answer, "handoff": False})
    else:
        # Suggest handoff
        return JsonResponse({
            "answer": "I couldn't find an answer. Would you like me to alert our team?",
            "handoff": True
        })


@csrf_exempt
def chat_alert(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    message = (data.get('message') or '').strip()
    contact = (data.get('contact') or '').strip()

    # Attempt to email site admins if configured
    try:
        from django.core.mail import mail_admins
        subject = "Bakery Chatbot Assistance Needed"
        body = f"Time: {timezone.now()}\nMessage: {message}\nContact: {contact or 'N/A'}"
        mail_admins(subject, body, fail_silently=True)
    except Exception:
        logger.warning("mail_admins failed or not configured")

    logger.info("Chat alert: %s | contact=%s", message, contact)
    return JsonResponse({"ok": True})
