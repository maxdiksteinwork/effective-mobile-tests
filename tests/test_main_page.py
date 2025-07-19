import pytest
import allure
from pages.main_page import MainPage


@pytest.fixture(scope="function")
def main_page(page):
    # Создаём объект страницы и переходим на главную
    mp = MainPage(page)
    mp.goto()
    return mp


@pytest.mark.parametrize("link_name", list(MainPage.links.keys()))
@allure.feature("Главная страница")
@allure.story("Навигация по разделам")
def test_navigation(main_page, page, link_name):
    # Кликаем по ссылке и получаем название раздела
    link_title = main_page.click_link(link_name)

    # Получаем ожидаемый якорь для проверки URL
    expected_anchor = main_page.get_expected_anchor(link_name)

    # Проверяем, что после клика URL содержит нужный якорь
    with allure.step(f"Переход в раздел '{link_title}'"):
        assert expected_anchor in page.url, f"URL {page.url} не содержит ожидаемый якорь {expected_anchor}"

    allure.dynamic.title(f"Проверка перехода в раздел '{link_title}'")