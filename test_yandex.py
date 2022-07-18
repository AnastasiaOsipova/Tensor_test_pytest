import pytest
from yandexPages import YandexHeadPage, YandexResultsPage, YandexImagePage, YandexImageResultsPage
from selenium import webdriver


class TestTensor:

    driver = None

    def setup_class(cls):
        path = 'chromedriver.exe'
        cls.driver = webdriver.Chrome(path)
        cls.yandex_head_page = YandexHeadPage(cls.driver)
        cls.yandex_results_page = YandexResultsPage(cls.driver)
        cls.yandex_image_page = YandexImagePage(cls.driver)
        cls.yandex_image_results_page = YandexImageResultsPage(cls.driver)
        cls.driver.maximize_window()

    def setup(self):
        #Зайти на yandex.ru
        url = 'https://yandex.ru/'
        self.driver.get(url)

    def test_01_search_tensor(self):
        """ищем в яндексе тензор и проверяем первую ссылку"""

        search_text = 'tensor'
      
        #Проверить наличия поля поиска, Ввести в поиск Тензор
        input_string = self.yandex_head_page.input_text(search_text)
        
        #проверяем, выпадает ли таблица с предложенными результатами
        self.yandex_head_page.check_suggest_table()
        
        #нажимаем ENTER
        self.yandex_head_page.click_enter(input_string)
        
        # Проверить, что 1 ссылка ведет на сайт tensor.ru
        self.yandex_results_page.check_first_link(search_text)

    
    def test_02_check_images(self):
        """заходим в яндекс картинки и проверяем их переключение"""

        category_number, image_number = 0, 0
        

        #Проверить, что ссылка «Картинки» присутствует на странице, кликаем на ссылку
        self.yandex_head_page.click_menu_item('Картинки')        

        #яндекс картинки открываются в другом окне, переключаемся между окнами 
        windows_list = self.driver.window_handles
        self.driver.switch_to.window(windows_list[1])

        #Проверить, что перешли на url https://yandex.ru/images/
        self.yandex_image_page.compare_url('https://yandex.ru/images/')

        #извлекаем название нужной категории
        category_name = self.yandex_image_page.get_category_name(category_number)

        #Открываем нужную категорию
        self.yandex_image_page.open_category(category_number)

        #текст из строки поиска можно извлечь только при перезагрузке страницы
        self.driver.refresh()

        #Проверить, что название категории отображается в поле поиска
        self.yandex_image_results_page.check_category_name(category_name)

        #открыть нужную картинку, проверить что она открылась
        self.yandex_image_results_page.open_image(image_number)
        
        #получаем адрес картинки
        first_image_url = self.yandex_image_results_page.get_src()
       
        #перелистнуть картинку на следующую, проверить что она открылась
        self.yandex_image_results_page.switch_next_image()

        #получаем адрес второй картинки
        second_image_url = self.yandex_image_results_page.get_src()
        
        #Проверить, что картинка сменилась
        self.yandex_image_results_page.check_disequality_image(first_image_url, second_image_url)

        #перелистнуть назад, на первую картинку, проверить что она открылась
        self.yandex_image_results_page.switch_last_image()

        #получаем адрес последней открытой картинки
        final_image_url = self.yandex_image_results_page.get_src()

        #проверить, что открылась первоначальная картинка
        self.yandex_image_results_page.check_equality_image(first_image_url, final_image_url)

    def teardown(self):
        windows_list = self.driver.window_handles
        if len(windows_list) == 2:
            self.driver.close()
            self.driver.switch_to.window(windows_list[0])     

    def teardown_class(cls):
        cls.driver.quit()   
