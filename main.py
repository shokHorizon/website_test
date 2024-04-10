import asyncio
from pyppeteer import launch
import unittest

class GitHubTestCase(unittest.TestCase):

    def setUp(self):
        self.browser = None
        self.page = None

    def tearDown(self):
        if self.browser:
            self.browser.close()

    async def test_case_1(self):
        """Проверка наличия элемента на странице"""
        self.browser = await launch()
        self.page = await self.browser.newPage()
        await self.page.goto('https://github.com')

        # 1. Наличие элемента на странице
        sign_up_button = await self.page.querySelector('.home-campaign-signup-button')
        self.assertIsNotNone(sign_up_button)

        # 2. Определенное значение у элемента
        sign_up_button_text = await self.page.evaluate('(element) => element.textContent', sign_up_button)
        self.assertEqual(sign_up_button_text, '\n  Sign up for GitHub\n  \n  \n')

        # 3. Состояние элемента
        sign_up_button_disabled = await self.page.evaluate('(element) => element.disabled', sign_up_button)
        self.assertFalse(sign_up_button_disabled)

    async def test_case_2(self):
        """Проверка формы поиска"""
        self.browser = await launch()
        self.page = await self.browser.newPage()
        await self.page.goto('https://github.com')

        # 1. Наличие элемента на странице
        search_input = await self.page.querySelector('.js-site-search-type-field')
        self.assertIsNotNone(search_input)

        # 2. Состояние элемента
        search_input_disabled = await self.page.evaluate('(element) => element.disabled', search_input)
        self.assertFalse(search_input_disabled)

        # 3. Ввод текста в поле поиска
        await search_input.type('pyppeteer')

    async def test_case_3(self):
        """Проверка списка репозиториев"""
        self.browser = await launch()
        self.page = await self.browser.newPage()
        await self.page.goto('https://github.com/trending')

        # 1. Наличие элемента на странице
        repo_list = await self.page.querySelectorAll('.Box-row')
        self.assertGreater(len(repo_list), 0)

        # 2. Определенное значение у элемента
        first_repo_name = await self.page.evaluate('(element) => element.textContent', repo_list[0])
        self.assertIn('Open-Sora-Plan', first_repo_name)

        # 3. Состояние элемента
        first_repo_disabled = await self.page.evaluate('(element) => element.disabled', repo_list[0])
        self.assertFalse(first_repo_disabled)

        # 4. Проверка, что элемент кликабелен
        await repo_list[0].click()
        self.assertIn('https://github.com/', self.page.url)

        # 5. Проверка, что элемент отображается на странице
        first_repo_visible = await self.page.evaluate('(element) => element.offsetParent !== null', repo_list[0])
        self.assertTrue(first_repo_visible)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    test_case_1 = loop.run_until_complete(GitHubTestCase().test_case_1())
    test_case_2 = loop.run_until_complete(GitHubTestCase().test_case_2())
    test_case_3 = loop.run_until_complete(GitHubTestCase().test_case_3())
