import requests
from .yougile_api_main import YouGileAPI


class GetYouGileTask:

    def __init__(self, token: str = None):

        self.base_url = "https://yougile.com/api-v2"
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}" if self.token else None,
            "Content-Type": "application/json"
        }

    def get_all_tasks(self):
        if not self.token:
            raise ValueError("Токен не установлен. Выполните аутентификацию.")

        url = f"{self.base_url}/tasks"  # Укажите конечную точку для задач
        response = requests.get(url, headers=self.headers)

        # Обработка ответа
        if response.status_code == 200:
            data = response.json()

            # Проверяем наличие задач в ответе
            content = data.get("content", [])
            if content:
                return content
            else:
                raise ValueError("Задачи отсутствуют в ответе.")
        else:
            response.raise_for_status()

    def get_task_by_title(self, tasks, title):
        # Ищем задачу по названию
        for task in tasks:
            if task.get("title") == title:
                #self.display_task_details(task)
                return task
        print(f"Задача с названием '{title}' не найдена.")
        return None

    # def display_task_details(self, task):
    #     # Отображение подробной информации о задаче
    #     title = task.get("title", "Без названия")
    #     timestamp = task.get("timestamp", "Дата не указана")
    #     task_id = task.get("id", "Без ID")
    #     description = task.get("description", "Без описания")
    #     completed = "Да" if task.get("completed", False) else "Нет"
    #     archived = "Да" if task.get("archived", False) else "Нет"
    #     due_date = task.get("dueDate", "Без срока")
    #
    #     print(f"Подробная информация о задаче '{title}':")
    #     print(f"  ID: {task_id}")
    #     print(f"  Описание: {description}")
    #     print(f"  Завершена: {completed}")
    #     print(f"  Архивирована: {archived}")
    #     print(f"  Срок: {due_date}")
    #     print("-" * 40)


if __name__ == "__main__":
    login = "kislyakim@gmail.com"  # Электронная почта пользователя
    password = "password1234"  # Пароль пользователя
    company_name = "adidas"  # Название компании

    yougile_api = YouGileAPI()

    try:

        company_id = yougile_api.get_company_id(login, password, company_name)
        print(f"ID компании '{company_name}': {company_id}")

        token = yougile_api.get_token(login, password, company_id)
        print(f"Токен успешно получен: {token}")

        tasks = yougile_api.get_all_tasks()

        task_title = input("Введите название задачи для поиска: ")
        yougile_api.get_task_by_title(tasks, task_title)

    except Exception as e:
        print(f"Ошибка: {e}")