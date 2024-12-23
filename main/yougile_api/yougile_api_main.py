import requests

class YouGileAPI:
    def __init__(self, token: str = None):

        self.base_url = "https://yougile.com/api-v2"
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}" if self.token else None,
            "Content-Type": "application/json"
        }

    def get_token(self, login: str, password: str, company_id: str):

        url = f"{self.base_url}/auth/keys/get"
        payload = {
            "login": login,
            "password": password,
            "companyId": company_id
        }

        # Отправка POST-запроса
        response = requests.post(url, json=payload, headers=self.headers)

        # Обработка ответа
        if response.status_code == 200:
            data = response.json()

            # Проверяем, что массив не пуст, и извлекаем ключ
            if data and isinstance(data, list) and "key" in data[0]:
                self.token = data[0]["key"]
                self.headers["Authorization"] = f"Bearer {self.token}"  # Добавляем токен в заголовки
                return self.token
            else:
                raise ValueError("Ключ (token) отсутствует в ответе.")
        else:
            response.raise_for_status()

    def get_company_id(self, login: str, password: str, company_name: str):

        url = f"{self.base_url}/auth/companies"
        payload = {
            "login": login,
            "password": password,
            "name": company_name
        }
        # Отправка POST-запроса
        response = requests.post(url, json=payload, headers=self.headers)

        # Обработка ответа
        if response.status_code == 200:
            data = response.json()
            content = data.get("content", [])
            # Проверяем, есть ли компании в ответе
            if content:
                company_id = content[0].get("id")
                if company_id:
                    return company_id
                else:
                    raise ValueError("ID компании отсутствует в ответе.")
            else:
                raise ValueError("Компания с указанным названием не найдена.")
        else:
            response.raise_for_status()


    def create_task(
            self,
            column_id: str,
            title: str,
            description: str = "string",
            archived: bool = False,
            completed: bool = False,
            subtasks: list = None,
            assigned: list = None,
            deadline: dict = None,
            time_tracking: dict = None,
            checklists: list = None,
            stickers: dict = None,
            color: str = "task-red",
            stopwatch: dict = None,
            timer: dict = None,
    ):

        if not self.token:
            raise ValueError("Токен не установлен. Выполните аутентификацию.")

        url = f"{self.base_url}/tasks"
        payload = {
            "columnId": column_id,
            "title": title,
            "description": description,
            "archived": archived,
            "completed": completed,
            "subtasks": subtasks or [],
            "assigned": assigned or [],
            "deadline": deadline,
            "timeTracking": time_tracking,
            "checklists": checklists or [],
            "stickers": stickers or {},
            "color": color,
            "stopwatch": stopwatch,
            "timer": timer,
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 201:
            task = response.json()
            print("Задача успешно создана:")
            self.display_task_details(task)
            return task
        else:
            response.raise_for_status()

    def get_boards(self):
        if not self.token:
            raise ValueError("Токен не установлен. Выполните аутентификацию.")

        url = f"{self.base_url}/boards"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            boards = response.json().get("content", [])
            if boards:
                print("Список досок:")
                for board in boards:
                    name = board.get("name", "Без названия")
                    board_id = board.get("id", "Без ID")
                    print(f"Доска: {name} (ID: {board_id})")
                return boards
            else:
                raise ValueError("Доски отсутствуют в ответе.")
        else:
            response.raise_for_status()



# if __name__ == "__main__":
#     login = "kislyakim@gmail.com"
#     password = "password1234"
#     company_name = "adidas"
#
#     yougile_api = YouGileAPI()
#
#     try:
#         company_id = yougile_api.get_company_id(login, password, company_name)
#         print(f"ID компании '{company_name}': {company_id}")
#
#         token = yougile_api.get_token(login, password, company_id)
#         print(f"Токен успешно получен: {token}")
#
#         boards = yougile_api.get_boards()
#
#         # Получите ID колонки (должен быть метод для получения колонок)
#         column_id = input("Введите ID колонки: ")
#
#         # Создаем задачу
#         task = yougile_api.create_task(
#             column_id=column_id,
#             title="Test Task",
#             description="This is a test task.",
#             archived=False,
#             completed=False,
#             subtasks=["0fe1e417-2415-4e76-932a-ca07a25d6c64", "f0118d9e-2888-48e4-a172-116085da4279"],
#             assigned=["80eed1bd-eda3-4991-ac17-09d28566749d"],
#             deadline={
#                 "deadline": 1653029146646,
#                 "startDate": 1653028146646,
#                 "withTime": True,
#             },
#             time_tracking={"plan": 10, "work": 5},
#             checklists=[
#                 {
#                     "title": "list 1",
#                     "items": [
#                         {"title": "option 1", "isCompleted": False},
#                         {"title": "option 2", "isCompleted": False},
#                     ],
#                 }
#             ],
#             stickers={
#                 "fbc30a9b-42d0-4cf7-80c0-31fb048346f9": "0baced9640b2",
#                 "645250ca-1ae8-4514-914d-c070351dd905": "815016901edd",
#             },
#             color="task-red",
#             stopwatch={"running": True},
#             timer={"running": True, "seconds": 600},
#         )
#         print("Созданная задача:", task)
#
#     except Exception as e:
#         print(f"Ошибка: {e}")


