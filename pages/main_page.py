import allure
from playwright.sync_api import Page, Locator


class MainPage:
    # Page Object для главной страницы effective-mobile.ru
    # Содержит локаторы и методы для навигации

    # Словарь: ключ ссылки -> (человеческое имя, якорь URL)
    links = {
        "home_link": ("Главная", "#main"),
        "about_us_link": ("О нас", "#about"),
        "services_link": ("Услуги", "#moreinfo"),
        "projects_link": ("Проекты", "#cases"),
        "reviews_link": ("Отзывы", "#Reviews"),
        "contacts_link": ("Контакты", "#contacts"),
        "choose_specialist_link": ("Выбрать специалиста", "#specialists"),
    }

    def __init__(self, page: Page):
        self.page = page

        # Инициализируем локаторы для ссылок
        self.home_link: Locator = page.locator('div.tn-atom a[href="#main"]', has_text='Effective Mobile').first
        self.about_us_link: Locator = page.locator('a.tn-atom[href="#about"]')
        self.services_link: Locator = page.locator('a.tn-atom[href="#moreinfo"]', has_text='[ Услуги ]')
        self.projects_link: Locator = page.locator('a.tn-atom[href="#cases"]')
        self.reviews_link: Locator = page.locator('a.tn-atom[href="#Reviews"]')
        self.contacts_link: Locator = page.locator('a.tn-atom[href="#contacts"]', has_text='[ Контакты ]')
        self.choose_specialist_link: Locator = page.locator('a.tn-atom[href="#specialists"]')

    def goto(self):
        # Переход на главную страницу сайта
        self.page.goto("https://effective-mobile.ru")

    def click_link(self, link_name: str) -> str:
        # Проверяем, что ссылка существует в объекте
        if not hasattr(self, link_name):
            raise ValueError(f"Неизвестное имя ссылки: {link_name}")

        # Получаем человеко-понятное название и локатор
        link_title = self.links.get(link_name, (link_name,))[0]
        locator = getattr(self, link_name)

        # Делаем клик с записью в отчёт allure
        with allure.step(f"Клик по разделу '{link_title}'"):
            locator.click()

        # Возвращаем название для использования в тестах/отчётах
        return link_title

    def get_expected_anchor(self, link_name: str) -> str:
        # Возвращаем ожидаемый якорь URL для данной ссылки
        return self.links.get(link_name, ("", ""))[1]
