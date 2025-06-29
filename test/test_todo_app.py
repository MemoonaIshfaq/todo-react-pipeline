import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager


class TestTodoApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")

        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.get("http://localhost:3000")  # Change if hosted elsewhere
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def fill_task_form(self, name, description, status, date):
        self.driver.find_element(By.NAME, "name").clear()
        self.driver.find_element(By.NAME, "description").clear()
        self.driver.find_element(By.NAME, "date").clear()

        self.driver.find_element(By.NAME, "name").send_keys(name)
        self.driver.find_element(By.NAME, "description").send_keys(description)
        Select(self.driver.find_element(By.NAME, "status")).select_by_visible_text(status)
        self.driver.find_element(By.NAME, "date").send_keys(date)

    def clear_task_form(self):
        self.driver.find_element(By.NAME, "name").clear()
        self.driver.find_element(By.NAME, "description").clear()
        self.driver.find_element(By.NAME, "date").clear()
        Select(self.driver.find_element(By.NAME, "status")).select_by_visible_text("Pending")

    def dismiss_alert_if_present(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass

    def test_1_page_title_exists(self):
        self.assertIn("To-Do", self.driver.page_source)
        print("Test case 1 passed: Page title exists")

    def test_2_task_name_input_present(self):
        self.assertTrue(self.driver.find_element(By.NAME, "name").is_displayed())
        print("Test case 2 passed: Task name input is present")

    def test_3_description_input_present(self):
        self.assertTrue(self.driver.find_element(By.NAME, "description").is_displayed())
        print("Test case 3 passed: Description input is present")

    def test_4_status_dropdown_present(self):
        self.assertTrue(self.driver.find_element(By.NAME, "status").is_displayed())
        print("Test case 4 passed: Status dropdown is present")

    def test_5_date_input_present(self):
        self.assertTrue(self.driver.find_element(By.NAME, "date").is_displayed())
        print("Test case 5 passed: Date input is present")

    def test_6_add_task_missing_required_fields(self):
        self.clear_task_form()
        self.driver.find_element(By.XPATH, "//button[text()='Add Task']").click()
        time.sleep(1)
        try:
            alert = self.driver.switch_to.alert
            self.assertEqual(alert.text, "Please fill all required fields")
            alert.accept()
            print("Test case 6 passed: Alert shown for missing required fields")
        except NoAlertPresentException:
            self.fail("Test case 6 failed: Expected alert not found")

    def test_7_add_valid_task(self):
        self.fill_task_form("Test Task", "Test Description", "Pending", "2025-12-31")
        self.driver.find_element(By.XPATH, "//button[text()='Add Task']").click()
        time.sleep(2)
        self.assertIn("Test Task", self.driver.page_source)
        print("Test case 7 passed: Valid task added successfully")

    def test_8_delete_task(self):
        time.sleep(2)
        delete_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Delete']")
        initial_count = len(delete_buttons)

        if initial_count == 0:
            self.test_7_add_valid_task()
            time.sleep(2)
            delete_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Delete']")
            initial_count = len(delete_buttons)

        delete_buttons[0].click()
        time.sleep(2)

        new_count = len(self.driver.find_elements(By.XPATH, "//button[text()='Delete']"))
        self.assertLess(new_count, initial_count)
        print("Test case 8 passed: Task deleted successfully")

    def test_9_status_change_option_exists(self):
        dropdown = Select(self.driver.find_element(By.NAME, "status"))
        options = [o.text for o in dropdown.options]
        self.assertIn("In Progress", options)
        self.assertIn("Completed", options)
        print("Test case 9 passed: Status options verified")

    def test_10_add_multiple_tasks(self):
        try:
            self.fill_task_form("Task 1", "First", "Completed", "2025-12-30")
            self.driver.find_element(By.XPATH, "//button[text()='Add Task']").click()
            time.sleep(2)

            self.clear_task_form()
            self.fill_task_form("Task 2", "Second", "In Progress", "2025-12-29")
            self.driver.find_element(By.XPATH, "//button[text()='Add Task']").click()
            time.sleep(2)

            self.assertIn("Task 1", self.driver.page_source)
            self.assertIn("Task 2", self.driver.page_source)
            print("Test case 10 passed: Multiple tasks added successfully")
        except UnexpectedAlertPresentException:
            self.dismiss_alert_if_present()
            self.fail("Test case 10 failed due to unexpected alert")


if __name__ == "__main__":
    unittest.main(verbosity=2)
