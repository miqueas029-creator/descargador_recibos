from playwright.sync_api import sync_playwright
import time
from datetime import datetime

def login():
    p = sync_playwright().start()
    context = p.chromium.launch_persistent_context(
        user_data_dir="perfil_finnegans",
        headless=False,
        channel="chrome",
        args=[
            "--disable-blink-features=AutomationControlled",
        ]
    )

    page = context.pages[0] if context.pages else context.new_page()
    page.goto(
        "https://services.finneg.com/login",
        wait_until="domcontentloaded")

    nombre_emp = page.locator("#logincompany")
    nombre_emp.click()
    nombre_emp.fill("UTDT")

    page.get_by_text("Ingresa usando Google", exact=True).click()

    page.locator("i.fas.fa-bars").wait_for(timeout=120_000)
    
    return p, page, context